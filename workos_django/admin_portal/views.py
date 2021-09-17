from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import os
import workos
from workos import client as workos_client
from workos import portal


workos.api_key = os.getenv('WORKOS_API_KEY')
workos.client_id = os.getenv('WORKOS_CLIENT_ID')

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.

workos.base_api_url = 'http://localhost:8000/' if settings.DEBUG else workos.base_api_url



def index(request):
    return render(request, 'admin_portal/index.html')


def provision_enterprise(request):
    organization_name =  request.POST['org']
    organization =  request.POST['domain']
    organization_domains = organization.split()

    organization = workos_client.organizations.create_organization({
        'name': organization_name,
        'domains': organization_domains
    })

    # You should persist `organization['id']` since it will be needed
    # to generate a Portal Link.
    global org_id 
    org_id = organization['id']

    return redirect('admin_portal')


def admin_portal(request):
    print('hit the admin portal route', org_id)

    portal_link = workos_client.portal.generate_link(
      organization=org_id, intent='sso'
    )
    print(portal_link)
    return redirect(portal_link['link'])
