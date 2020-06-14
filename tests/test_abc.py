from datetime import datetime, timezone

import mock
import pytest

from news_scraper.sites.abc import (
    get_articles
)


def mock_response(status_code, html):
    resp = mock.MagicMock()
    resp.status_code = status_code
    resp.text = html
    return resp


@mock.patch('requests.get')
def test_get_articles(mock_requests):
    response200 = mock_response(200, """
        <html>
            <body>
                <div class="c66l">
                    <div
                        class="inline-content uberlist ng3ts show-for-national avoid-orphans copyfit-image-ratio dividers default-image-width-160 heading-labels new-content-check show-teaser-related-doctypes"
                    >
                        <div class="section module-body">
                            <ol
                                data-cmid="5513552"
                                data-cmjson=""
                                data-volume=""
                            >
                                <li
                                    class="doctype-article"
                                    data-image-cmid="12341522"
                                    data-cmid="12341558"
                                    data-importance="4"
                                    data-first-published="2020-06-13T08:25+1000"
                                    data-last-published="2020-06-13T09:15+1000"
                                >
                                    <h3>
                                        <a href="/news/2020-06-13/headline-1">Headline 1</a>
                                    </h3>
                                    <p>Summary 1</p>
                                </li>
                                <li
                                    class="doctype-article"
                                    data-image-cmid="12349436"
                                    data-cmid="12349444"
                                    data-importance="4"
                                    data-first-published="2020-06-13T05:10+1000"
                                    data-last-published="2020-06-13T08:28+1000"
                                >
                                    <h3>
                                        <a href="/news/2020-06-13/headline-2">Headline 2</a>
                                    </h3>
                                    <p>Summary 2</p>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    """)
    response500 = mock_response(500, 'Internal Server Error')
    date_scraped = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    # Check if data is extracted correctly from html
    mock_requests.side_effect = [response200]
    result = get_articles(date_scraped)
    expected_result = [
        {
            'headline': 'Headline 1',
            'date_first_published': '2020-06-13T08:25+1000',
            'date_last_published': '2020-06-13T09:15+1000',
            'summary': 'Summary 1',
            'url': 'https://www.abc.net.au/news/2020-06-13/headline-1',
            'type': 'main',
            'date_scraped': date_scraped
        },
            {
            'headline': 'Headline 2',
            'date_first_published': '2020-06-13T05:10+1000',
            'date_last_published': '2020-06-13T08:28+1000',
            'summary': 'Summary 2',
            'url': 'https://www.abc.net.au/news/2020-06-13/headline-2',
            'type': 'main',
            'date_scraped': date_scraped
        },
    ]
    assert(result == expected_result)
    # Check exception is raised
    mock_requests.side_effect = [response500]
    with pytest.raises(Exception) as e:
        get_articles(date_scraped)
    assert str(e.value) == 'Invalid status code: 500'
