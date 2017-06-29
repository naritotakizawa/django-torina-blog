"""Hello Analytics Reporting API V4."""
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')


def initialize_analyticsreporting():
    """Initializes an analyticsreporting service object.

    Returns:   analytics an authorized analyticsreporting service
    object.

    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        settings.SERVICE_ACCOUNT_EMAIL, settings.KEY_FILE_LOCATION,
        scopes=SCOPES
    )

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http,
                      discoveryServiceUrl=DISCOVERY_URI)

    return analytics


def get_report(analytics):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': settings.VIEW_ID,
                    'pageSize': 10,
                    'dateRanges': [
                        {'startDate': '7daysAgo', 'endDate': 'today'}
                    ],
                    'metrics': [
                        {'expression': 'ga:pageviews'},
                    ],
                    'dimensions': [
                        {'name': 'ga:pagePath'}, {'name': 'ga:pageTitle'}
                    ],
                    'orderBys': [
                        {
                            'fieldName': 'ga:pageviews',
                            'sortOrder': 'DESCENDING'
                        },
                    ]
                }]
        }
    ).execute()


def get_10_popular():
    """過去1週間の人気ページを10件返す.

    URL、ページタイトル、PV数をyieldで返します

    """
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    for report in response.get('reports', []):
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            url = row['dimensions'][0]
            title = row['dimensions'][1]
            page_view = row['metrics'][0]['values'][0]
            yield url, title, int(page_view)


if __name__ == '__main__':
    for url, title, page_view in get_10_popular():
        print(url, title, page_view)
