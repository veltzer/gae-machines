#!/usr/bin/env python

"""
Script to get the cpu quota for a specfic region
"""

from google.cloud import cloudquotas_v1
import google.auth


def get_cpu_quota_for_region(project_id, _region):
    client = cloudquotas_v1.CloudQuotasClient()
    request = cloudquotas_v1.GetQuotaInfoRequest(
        # name= f"projects/{project_id}/locations/{region}"
        name=f"projects/{project_id}/locations/global/services/compute.googleapis.com/quotaInfos/CPUs"
    )
    response = client.get_quota_info(request=request)
    print(response)

def main():
    _, project_id = google.auth.default()
    region = "us-central1"
    get_cpu_quota_for_region(project_id, region)


if __name__ == "__main__":
    main()
