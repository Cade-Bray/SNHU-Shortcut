from dash import html, Dash, dcc, dash_table, Input, Output, State
import kuali_driver as kd
import base64

#########################
# Dashboard Layout / View
#########################

def main():
    """
    Main function to create and run the Dash application.
    :return: void
    """

    # Load courses from Kuali
    courses = kd.load_courses()

    # Create a Dash application
    app = Dash(
        "SNHU Shortcut Dash App",
        assets_folder=".images",
        assets_url_path="/.images",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
        ],
    )
    app.title = "SNHU Shortcut"

    # Load the logo image
    logo_path = ".images/Logo.jpg"
    with open(logo_path, "rb") as logo_file:
        logo_data = logo_file.read()
    logo_encoded = base64.b64encode(logo_data).decode("utf-8")

    app.layout = html.Div(
        children = [
            html.Div(
                style = {'display': 'flex', 'alignItems': 'center', 'position': 'relative'},
                children = [
                    html.A(
                        href='https://www.snhu.edu',
                        children=[
                            html.Img(
                                src='data:image/png;base64,{}'.format(logo_encoded),
                                style={'height': '50px', 'marginRight': 'auto'}
                            )
                        ]
                    ),
                    html.Div(
                        children = [
                            html.B(
                                html.H3(
                                    'Assisting students with finding course alternatives',
                                    style={'margin': '0 20px'}
                                )
                            ),
                        ],
                        style = {'display': 'flex', 'flexDirection': 'column', 'alignItems': 'left'}
                    ),
                    html.Div(
                        children = [
                            html.A(
                                href = "https://www.paypal.com/donate/?business=EKWEKWDS86Q3A&no_recurring=1&item_name="
                                       "I%27m+glad+you%27ve+found+SNHU+shortcut+useful+and+thank+you+for+buying+me+a+"
                                       "coffee%21&currency_code=USD",
                                title = "PayPal - The safer, easier way to pay online!",
                                children = [
                                    html.Img(
                                        src = "https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif",
                                        style = {'padding': '20px'}
                                    )
                                ]
                            )
                        ],
                        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'right'}
                    )
                ]
            ),
            html.Hr(),
            html.Div(
                children = [
                    html.H2("What are course alternatives at SNHU?"),
                    html.P("Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."),
                    html.P("Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."),
                    html.Br()
                ],
                style = {'textAlign': 'center', 'margin': '20px'}
            ),
            html.Hr(),
            html.Div(
                [
                    html.Br(),
                    html.Label("Enter your course ID (EX101):"),
                    dcc.Input(id="course_id", type="text", value=""),
                    html.Button("Submit", id="submit_button", n_clicks=0),
                ]
            ),
            html.Div(id="output_div"),
            html.Br(),
            html.Hr(),
            html.Div(
                children = [
                    html.H2("Disclaimer"),
                    html.P("The software provided in this repository/site is offered \"as-is\" without any warranties or "
                           "guarantees of any kind, either express or implied. The author(s) of this software shall not "
                           "be held liable for any damages, losses, or issues arising from the use or inability to use "
                           "this software, including but not limited to direct, indirect, incidental, special, "
                           "consequential, or punitive damages. This site is not affiliated with or endorsed by "
                           "Southern New Hampshire University (SNHU) or any other institution. The information provided "
                           "here is for educational and informational purposes only. "
                           "By using this software, you acknowledge that you do so at your own risk. It is your "
                           "responsibility to ensure that the software meets your requirements and to test it in a safe "
                           "environment before deploying it in a production setting. The author(s) do not guarantee that "
                           "the information provided here is accurate, complete, or up-to-date. To understand if this "
                            "software is right for you, please consult with a qualified professional at SNHU. "
                           "The author(s) make no representations about the suitability, reliability, availability, "
                           "timeliness, or accuracy of the software for any purpose."),
                    html.P("If you have any questions or concerns regarding this software, please contact the author(s)"
                           " directly at:"),
                    html.A(href="mailto:Bray.Cade@gmail.com", target="_blank",
                           children=[
                               html.P("Bray.Cade@gmail.com")
                           ]
                    )
                ],
                style = {'textAlign': 'center', 'margin': '20px'}
            )
        ]
    )

    # Hit the go button!
    app.run(debug=True)


if __name__ == "__main__":
    main()