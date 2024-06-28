"""header"""

from dash import html


def header(title: str, strong_class: str = "", background_colour: str = None):
    """
    The header component, shared across all dashboard views. Includes optional strong_class
    parameter to provide extra styling in the form of a class.
    Includes optional background_colour parameter to override default black background colour.

    Based on the header component provided by the GOV.UK Design System.
    https://design-system.service.gov.uk/components/header/
    """
    header_style = {"backgroundColor": background_colour} if background_colour else {}

    return html.Header(
        html.Div(
            html.Div(
                [
                    html.Img(
                        src="assets\\images\\DLUHC_WHITE_Master_AW_sm.png",
                        srcSet="assets\\images\\DLUHC_WHITE_Master_AW_sm.png 490w",
                        sizes="(min-width: 600px) 200px, 30vw",
                        className="header-image",
                        style={"maxWidth": "200px"},
                        alt="Department for Levelling Up, Housing & Communities",
                    ),
                    html.A(
                        title,
                        href="/",
                        className=" ".join(
                            [
                                "govuk-header__link",
                                "govuk-header__link--service-name",
                                "dashboard-title",
                            ],
                        ),
                    ),
                    html.Div(
                        [
                            html.Strong(
                                "OFFICIAL",
                                className="govuk-tag protective-marking",
                                id="protective-marking",
                            )
                        ],
                        className=f"{strong_class}",
                    ),
                    html.Button(
                        "Menu ▼",
                        id="mobile-menu-btn",
                        className="mobile-menu-button govuk-button",
                    ),
                ],
                className="govuk-header__content",
            ),
            className="govuk-header__container govuk-width-container",
        ),
        className="govuk-header",
        role="banner",
        style=header_style,
        **{"data-module": "govuk-header"},
    )
