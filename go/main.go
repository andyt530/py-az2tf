// Copyright © 2018 DeployView Limited hello@deployview.com
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// naming conventions embedded
// modularizing
// sre 12 checklist for transition
// aws contact for aws style modules

package main

import (
	"context"
	"deployview/internal/config"
	"deployview/internal/iam"
	"deployview/internal/util"
	"flag"
	"html/template"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"

	"github.com/Azure/azure-sdk-for-go/profiles/latest/resources/mgmt/resources"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/azure"
	"github.com/Azure/go-autorest/autorest/to"
	"github.com/Azure/go-autorest/autorest/validation"
)

// Returns terraform resource type
func GetTerraformResoureType(azureResourceType string) string {
	switch azureResourceType {
	case "Microsoft.Network/networkInterfaces":
		azureResourceType = "azurerm_network_interface"
	case "Microsoft.Network/networkSecurityGroups":
		azureResourceType = "azurerm_network_security_group"
	case "Microsoft.Network/publicIPAddresses":
		azureResourceType = "azurerm_public_ip"
	default:
		azureResourceType = azureResourceType
	}
	return azureResourceType
}

// Returns supported api version
func GetSupportedApiVersion(resourceType string) string {
	var apiVersion = "2018-08-01"
	switch resourceType {
	case "vaults":
		apiVersion = "2018-01-10"
	case "storageAccounts":
		apiVersion = "2018-07-01"
	case "virtualMachines":
		apiVersion = "2018-06-01"
	case "disks":
		apiVersion = "2018-06-01"
	case "solutions":
		apiVersion = "2015-11-01-preview"
	case "workspaces":
		apiVersion = "2015-03-20"
	case "projects":
		apiVersion = "2018-02-02"
	case "snapshots":
		apiVersion = "2018-06-01"
	case "availabilitySets":
		apiVersion = "2018-06-01"
	case "databaseAccounts":
		apiVersion = "2016-03-31"
	case "managedClusters":
		apiVersion = "2018-03-31"
	case "images":
		apiVersion = "2018-06-01"
	case "registries":
		apiVersion = "2017-10-01"
	case "scheduledqueryrules":
		apiVersion = "2018-04-16"
	case "actiongroups":
		apiVersion = "2018-03-01"
	case "automationAccounts":
		apiVersion = "2018-06-30"
	case "restorePointCollections":
		apiVersion = "2018-06-01"
	case "schedules":
		apiVersion = "2016-05-15" //2018-10-15-preview
	default:
		apiVersion = "2018-08-01"
	}
	return apiVersion
}

// Output terraform config
func Export() {
	err := setupEnvironment()

	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Second)
	defer cancel()

	_, err = ListGroups(ctx)
	if err != nil {
		util.PrintAndLog(err.Error())
	}

	type Plan struct {
		// Name - The plan ID.
		Name *string `json:"name,omitempty"`
		// Publisher - The publisher ID.
		Publisher *string `json:"publisher,omitempty"`
		// Product - The offer ID.
		Product *string `json:"product,omitempty"`
		// PromotionCode - The promotion code.
		PromotionCode *string `json:"promotionCode,omitempty"`
		// Version - The plan's version.
		Version *string `json:"version,omitempty"`
	}

	// Sku SKU for the resource.
	type Sku struct {
		// Name - The SKU name.
		Name *string `json:"name,omitempty"`
		// Tier - The SKU tier.
		Tier *string `json:"tier,omitempty"`
		// Size - The SKU size.
		Size *string `json:"size,omitempty"`
		// Family - The SKU family.
		Family *string `json:"family,omitempty"`
		// Model - The SKU model.
		Model *string `json:"model,omitempty"`
		// Capacity - The SKU capacity.
		Capacity *int32 `json:"capacity,omitempty"`
	}

	// ResourceIdentityType enumerates the values for resource identity type.
	type ResourceIdentityType string

	// Identity identity for the resource.
	type Identity struct {
		// PrincipalID - The principal ID of resource identity.
		PrincipalID *string `json:"principalId,omitempty"`
		// TenantID - The tenant ID of resource.
		TenantID *string `json:"tenantId,omitempty"`
		// Type - The identity type. Possible values include: 'SystemAssigned', 'UserAssigned', 'SystemAssignedUserAssigned', 'None'
		Type ResourceIdentityType `json:"type,omitempty"`
	}

	// Group is resource group information.
	type Group struct {
		autorest.Response `json:"-"`
		ID                *string            `json:"id,omitempty"`
		Name              *string            `json:"name,omitempty"`
		Location          *string            `json:"location,omitempty"`
		ManagedBy         *string            `json:"managedBy,omitempty"`
		Tags              map[string]*string `json:"tags,omitempty"`
	}

	tmplg, err := template.ParseFiles("terraform_resource_group.tmpl")

	// Generates Terraform config for Azure Resource Groups
	for list, err := ListGroups(ctx); list.NotDone(); err = list.Next() {
		if err != nil {
			log.Printf("\n# resource group got error: %s\n", err)
			log.Printf("\n# Debug resource group: %v\n", list.Value())
		} else {
			resource := Group{list.Value().Response, list.Value().ID, list.Value().Name, list.Value().Location, list.Value().ManagedBy, list.Value().Tags}
			err = tmplg.ExecuteTemplate(os.Stdout, "terraform_resource_group.tmpl", resource)
			resourcesClient := getResourcesClient()
			var groupname = *list.Value().Name

			const tmplr0 = `resource "{{.}}"`
			const tmplr1 = ` "{{.Name}}" {
{{if .Name}}  name     = "{{ .Name }}"
{{end}}`
			const tmplr2 = `{{ if . }}  resource_group_name     = "{{ . }}"
{{ end }}`
			const tmplr3 = `{{if .Plan}} plan = "{{ .Plan }}"{{end}}{{ range $key, $value := .Properties }}  {{ $key }} = "{{ $value }}"
{{ end }}{{if .Kind}}  kind = "{{ .Kind }}"
{{end}}{{if .ManagedBy}}  managedby = "{{ .ManagedBy }}"
{{end}}{{if .Identity}}  identity = "{{ .Identity }}"
{{end}}{{if .Location}}  location = "{{ .Location }}"{{end}}
}
`
			for listre, err := resourcesClient.ListByResourceGroupComplete(ctx, groupname, "", "", nil); listre.NotDone(); err = listre.Next() {
				if err != nil {
					log.Printf("\n# list resource got error: %s\n", err)
				} else {
					var retype = strings.Split(*listre.Value().Type, "/")
					var rename = strings.Split(*listre.Value().Name, "/")
					resourceproperties, err := GetResource(ctx, groupname, retype[0], retype[1], rename[0], GetSupportedApiVersion(retype[1]))
					if err != nil {
						log.Printf("\n# resource properties got error: %s\n", err)
						log.Printf("\n# Debug resource properties: %v\n", resourceproperties)
						log.Printf("\n#  %s %s %s %s\n", retype[1], retype[0], groupname, rename)
					} else {
						tmplr0 := template.Must(template.New("tmplr0").Parse(tmplr0))
						err = tmplr0.Execute(os.Stdout, GetTerraformResoureType(*resourceproperties.Type))
						if err != nil {
							log.Printf("\n# got error: %s\n", err)
						}
						tmplr1 := template.Must(template.New("tmplr1").Parse(tmplr1))
						err = tmplr1.Execute(os.Stdout, resourceproperties)
						if err != nil {
							log.Printf("\n# got error: %s\n", err)
						}
						tmplr2 := template.Must(template.New("tmplr2").Parse(tmplr2))
						err = tmplr2.Execute(os.Stdout, groupname)
						if err != nil {
							log.Printf("\n# got error: %s\n", err)
						}
						tmplr3 := template.Must(template.New("tmplr3").Parse(tmplr3))
						err = tmplr3.Execute(os.Stdout, resourceproperties)
						if err != nil {
							log.Printf("\n# got error: %s\n", err)
						}
					}
				}
			}
		}
	}

}

func getResourcesClient() resources.Client {
	resourcesClient := resources.NewClient(config.SubscriptionID())
	a, _ := iam.GetResourceManagementAuthorizer()
	resourcesClient.Authorizer = a
	resourcesClient.AddToUserAgent(config.UserAgent())
	return resourcesClient
}

func setupEnvironment() error {
	err1 := config.ParseEnvironment()
	err2 := config.AddFlags()

	for _, err := range []error{err1, err2} {
		if err != nil {
			return err
		}
	}

	flag.Parse()
	return nil
}

func getGroupsClient() resources.GroupsClient {
	groupsClient := resources.NewGroupsClient(config.SubscriptionID())
	a, err := iam.GetResourceManagementAuthorizer()
	if err != nil {
		log.Fatalf("failed to initialize authorizer: %v\n", err)
	}
	groupsClient.Authorizer = a
	groupsClient.AddToUserAgent(config.UserAgent())
	return groupsClient
}

// GetGroup gets info on the resource group in use
func GetGroup(ctx context.Context) (resources.Group, error) {
	groupsClient := getGroupsClient()
	return groupsClient.Get(ctx, config.GroupName())
}

// ListGroups gets an interator that gets all resource groups in the subscription
func ListGroups(ctx context.Context) (resources.GroupListResultIterator, error) {
	groupsClient := getGroupsClient()
	return groupsClient.ListComplete(ctx, "", nil)
}

// ListResources gets an interator that gets all resources in the subscription
func ListResouces(ctx context.Context) (resources.ListResultIterator, error) {
	resourcesClient := getResourcesClient()
	return resourcesClient.ListComplete(ctx, "", "", nil)
}

// BaseClient is the base client for Resources.
type BaseClient struct {
	autorest.Client
	BaseURI        string
	SubscriptionID string
}

// Client is the provides operations for working with resources and resource groups.
type Client struct {
	BaseClient
}

// ListResultIterator provides access to a complete listing of GenericResource values.
type ListResultIterator struct {
	i    int
	page ListResultPage
}

// ListResultPage contains a page of GenericResource values.
type ListResultPage struct {
	fn func(ListResult) (ListResult, error)
	lr ListResult
}

// Plan plan for the resource.
type Plan struct {
	// Name - The plan ID.
	Name *string `json:"name,omitempty"`
	// Publisher - The publisher ID.
	Publisher *string `json:"publisher,omitempty"`
	// Product - The offer ID.
	Product *string `json:"product,omitempty"`
	// PromotionCode - The promotion code.
	PromotionCode *string `json:"promotionCode,omitempty"`
	// Version - The plan's version.
	Version *string `json:"version,omitempty"`
}

// Sku SKU for the resource.
type Sku struct {
	// Name - The SKU name.
	Name *string `json:"name,omitempty"`
	// Tier - The SKU tier.
	Tier *string `json:"tier,omitempty"`
	// Size - The SKU size.
	Size *string `json:"size,omitempty"`
	// Family - The SKU family.
	Family *string `json:"family,omitempty"`
	// Model - The SKU model.
	Model *string `json:"model,omitempty"`
	// Capacity - The SKU capacity.
	Capacity *int32 `json:"capacity,omitempty"`
}

// ResourceIdentityType enumerates the values for resource identity type.
type ResourceIdentityType string

// Identity identity for the resource.
type Identity struct {
	// PrincipalID - The principal ID of resource identity.
	PrincipalID *string `json:"principalId,omitempty"`
	// TenantID - The tenant ID of resource.
	TenantID *string `json:"tenantId,omitempty"`
	// Type - The identity type. Possible values include: 'SystemAssigned', 'UserAssigned', 'SystemAssignedUserAssigned', 'None'
	Type ResourceIdentityType `json:"type,omitempty"`
}

// GenericResource resource information.
type GenericResource struct {
	autorest.Response `json:"-"`
	// Plan - The plan of the resource.
	Plan *Plan `json:"plan,omitempty"`
	// Properties - The resource properties.
	Properties interface{} `json:"properties,omitempty"`
	// Kind - The kind of the resource.
	Kind *string `json:"kind,omitempty"`
	// ManagedBy - ID of the resource that manages this resource.
	ManagedBy *string `json:"managedBy,omitempty"`
	// Sku - The SKU of the resource.
	Sku *Sku `json:"sku,omitempty"`
	// Identity - The identity of the resource.
	Identity *Identity `json:"identity,omitempty"`
	// ID - Resource ID
	ID *string `json:"id,omitempty"`
	// Name - Resource name
	Name string `json:"name,omitempty"`
	// Type - Resource type
	Type *string `json:"type,omitempty"`
	// Location - Resource location
	Location *string `json:"location,omitempty"`
	// Tags - Resource tags
	Tags map[string]*string `json:"tags"`
}

// ListResult list of resource groups.
type ListResult struct {
	autorest.Response `json:"-"`
	// Value - An array of resources.
	Value *[]GenericResource `json:"value,omitempty"`
	// NextLink - The URL to use for getting the next set of results.
	NextLink *string `json:"nextLink,omitempty"`
}

// ListByResourceGroupPreparer prepares the ListByResourceGroup request.
func (client Client) ListByResourceGroupPreparer(ctx context.Context, resourceGroupName string, filter string, expand string, top *int32) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2018-03-31"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}
	if len(filter) > 0 {
		queryParameters["$filter"] = autorest.Encode("query", filter)
	}
	if len(expand) > 0 {
		queryParameters["$expand"] = autorest.Encode("query", expand)
	}
	if top != nil {
		queryParameters["$top"] = autorest.Encode("query", *top)
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/resources", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// ListByResourceGroupSender sends the ListByResourceGroup request. The method will close the
// http.Response Body if it receives an error.
func (client Client) ListByResourceGroupSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// ListByResourceGroupResponder handles the response to the ListByResourceGroup request. The method always
// closes the http.Response Body.
func (client Client) ListByResourceGroupResponder(resp *http.Response) (result ListResult, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// listResultPreparer prepares a request to retrieve the next set of results.
// It returns nil if no more results exist.
func (lr ListResult) listResultPreparer() (*http.Request, error) {
	if lr.NextLink == nil || len(to.String(lr.NextLink)) < 1 {
		return nil, nil
	}
	return autorest.Prepare(&http.Request{},
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(to.String(lr.NextLink)))
}

// listByResourceGroupNextResults retrieves the next set of results, if any.
func (client Client) listByResourceGroupNextResults(lastResults ListResult) (result ListResult, err error) {
	req, err := lastResults.listResultPreparer()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "resources.Client", "listByResourceGroupNextResults", nil, "Failure preparing next results request")
	}
	if req == nil {
		return
	}
	resp, err := client.ListByResourceGroupSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		return result, autorest.NewErrorWithError(err, "resources.Client", "listByResourceGroupNextResults", resp, "Failure sending next results request")
	}
	result, err = client.ListByResourceGroupResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "resources.Client", "listByResourceGroupNextResults", resp, "Failure responding to next results request")
	}
	return
}

// ListByResourceGroup get all the resources for a resource group.
// Parameters:
// resourceGroupName - the resource group with the resources to get.
// filter - the filter to apply on the operation.
// expand - the $expand query parameter
// top - the number of results to return. If null is passed, returns all resources.
func (client Client) ListByResourceGroup(ctx context.Context, resourceGroupName string, filter string, expand string, top *int32) (result ListResultPage, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}}}); err != nil {
		return result, validation.NewError("resources.Client", "ListByResourceGroup", err.Error())
	}

	result.fn = client.listByResourceGroupNextResults
	req, err := client.ListByResourceGroupPreparer(ctx, resourceGroupName, filter, expand, top)
	if err != nil {
		err = autorest.NewErrorWithError(err, "resources.Client", "ListByResourceGroup", nil, "Failure preparing request")
		return
	}

	resp, err := client.ListByResourceGroupSender(req)
	if err != nil {
		result.lr.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "resources.Client", "ListByResourceGroup", resp, "Failure sending request")
		return
	}

	result.lr, err = client.ListByResourceGroupResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "resources.Client", "ListByResourceGroup", resp, "Failure responding to request")
	}

	return
}

// ListByResourceGroupComplete enumerates all values, automatically crossing page boundaries as required.
func (client Client) ListByResourceGroupComplete(ctx context.Context, resourceGroupName string, filter string, expand string, top *int32) (result ListResultIterator, err error) {
	result.page, err = client.ListByResourceGroup(ctx, resourceGroupName, filter, expand, top)
	return
}

// Get gets a resource.
// Parameters:
// resourceGroupName - the name of the resource group containing the resource to get. The name is case
// insensitive.
// resourceProviderNamespace - the namespace of the resource provider.
// parentResourcePath - the parent resource identity.
// resourceType - the resource type of the resource.
// resourceName - the name of the resource to get.
func (client Client) Get(ctx context.Context, resourceGroupName string, resourceProviderNamespace string, parentResourcePath string, resourceType string, resourceName string) (result GenericResource, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}}}); err != nil {
		return result, validation.NewError("resources.Client", "Get", err.Error())
	}

	req, err := client.GetPreparer(ctx, resourceGroupName, resourceProviderNamespace, parentResourcePath, resourceType, resourceName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "resources.Client", "Get", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "resources.Client", "Get", resp, "Failure sending request")
		return
	}

	result, err = client.GetResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "resources.Client", "Get", resp, "Failure responding to request")
	}

	return
}

// GetSender sends the Get request. The method will close the
// http.Response Body if it receives an error.
func (client Client) GetSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// GetResponder handles the response to the Get request. The method always
// closes the http.Response Body.
func (client Client) GetResponder(resp *http.Response) (result GenericResource, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetPreparer prepares the Get request.
func (client Client) GetPreparer(ctx context.Context, resourceGroupName string, resourceProviderNamespace string, parentResourcePath string, resourceType string, resourceName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"parentResourcePath":        parentResourcePath,
		"resourceGroupName":         autorest.Encode("path", resourceGroupName),
		"resourceName":              autorest.Encode("path", resourceName),
		"resourceProviderNamespace": autorest.Encode("path", resourceProviderNamespace),
		"resourceType":              resourceType,
		"subscriptionId":            autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2018-02-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// WithAPIVersion returns a prepare decorator that changes the request's query for api-version
// This can be set up as a client's RequestInspector.
func WithAPIVersion(apiVersion string) autorest.PrepareDecorator {
	return func(p autorest.Preparer) autorest.Preparer {
		return autorest.PreparerFunc(func(r *http.Request) (*http.Request, error) {
			r, err := p.Prepare(r)
			if err == nil {
				v := r.URL.Query()
				d, err := url.QueryUnescape(apiVersion)
				if err != nil {
					return r, err
				}
				v.Set("api-version", d)
				r.URL.RawQuery = v.Encode()
			}
			return r, err
		})
	}
}

// GetResource gets a resource, the generic way.
// The API version parameter overrides the API version in
// the SDK, this is needed because not all resources are
// supported on all API versions.
func GetResource(ctx context.Context, resourceGroupName, resourceProvider, resourceType, resourceName, apiVersion string) (resources.GenericResource, error) {
	resourcesClient := getResourcesClient()
	resourcesClient.RequestInspector = WithAPIVersion(apiVersion)

	return resourcesClient.Get(
		ctx,
		resourceGroupName,
		resourceProvider,
		"",
		resourceType,
		resourceName,
	)
}

func main() {
	Export()
}
