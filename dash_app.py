import os
from dash import html, Dash, dcc, dash_table, Input, Output, State
import kuali_driver as kd
import base64

#########################
# Dashboard Layout / View
#########################

# Making it the app global so it can be used in the callback
app = Dash(
        "SNHU Shortcut Dash App",
        assets_folder=".images",
        assets_url_path="/.images",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
        ],
    )
server = app.server

def main():
    """
    Main function to create and run the Dash application.
    :return: void
    """

    # Load courses from Kuali
    courses = kd.load_courses()

    # Create a Dash application
    app.title = "SNHU Shortcut"

    # Load the logo image
    logo_path = ".images/Logo.jpg"
    with open(logo_path, "rb") as logo_file:
        logo_data = logo_file.read()
    logo_encoded = base64.b64encode(logo_data).decode("utf-8")

    app.layout = html.Div(
        children = [
            html.Div(
                style= {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between',
                        'alignItems': 'center', 'padding': '10px', 'flexWrap': 'wrap', 'overflow': 'hidden'},
                children=[
                    html.Div(
                        style = {'display': 'flex','flexDirection': 'row' , 'alignItems': 'center', 'position': 'relative'},
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
                                            'Assisting Students with Finding Course Alternatives',
                                            style={'margin': '0 20px'}
                                        )
                                    ),
                                ],
                                style = {'display': 'flex', 'flexDirection': 'column', 'alignItems': 'left'}
                            ),
                        ],
                    ),
                    html.Div(
                        id= 'header_buttons',
                        style = {'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'},
                        children=[
                            html.Div(
                                style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'right',
                                       'justifyContent': 'flex-end'},
                                children=[
                                    html.A(
                                        href='https://github.com/Cade-Bray/SNHU-Shortcut',
                                        children=[
                                            html.Img(
                                                src='https://img.shields.io/github/stars/Cade-Bray/SNHU-Shortcut?style=social',
                                                style={'height': '30px', 'marginRight': '10px'}
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.A(
                                        href="https://www.paypal.com/donate/?business=EKWEKWDS86Q3A&no_recurring=1&item_name="
                                             "I%27m+glad+you%27ve+found+SNHU+shortcut+useful+and+thank+you+for+buying+me+a+"
                                             "coffee%21&currency_code=USD",
                                        title="PayPal - The safer, easier way to pay online!",
                                        children=[
                                            html.Img(
                                                src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif",
                                                style={'padding': '20px'}
                                            )
                                        ]
                                    )
                                ],
                                style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'right'}
                            ),
                            dcc.Interval(id="resize-interval", interval=1000, n_intervals=0)
                        ]
                    )
                ]
            ),
            html.Hr(),
            html.Div(
                children = [
                    html.H2("What are course alternatives at SNHU?"),
                    html.P("Course alternatives at SNHU are a way for students to find academic outlets outside of the "
                           "traditional course offerings. These alternatives are mostly certifications."
                           " They are designed to help students gain practical skills and knowledge that can be applied "
                           "in the real world. Additionally, they're often highly valued by employers which can add to"
                           " your post graduation resume. It's common for students to take these to satisfy courses in a"
                           " more cost effective way or to allow for more flexibility in their in their education. Some"
                           "certifications can even be used to satisfy multiple courses at once. Some certifications "
                           "can even be completed in a fraction of the time it would take to complete a course. Allowing"
                           " more experienced students to graduate faster."),
                    html.P([
                        "A full list of certifications can be found on the ",
                        html.A(
                            href="https://www.snhu.edu/admission/transferring-credits/work-life-experience/#/experiences",
                            target="_blank",
                            children=["SNHU certifications page"]
                        ),
                        ". You may be wondering how this website differs from the SNHU certifications page. The SNHU "
                        "certification page is structured in such a way that it is difficult to find certifcations that"
                        " satisfy a specific course. This website allows you to enter a course ID and find all instantly"
                        ". Please note that this website is updating daily and may not have the most up to date depending"
                        "on the most recent update to the SNHU certifications page."
                    ]),
                    html.Br()
                ],
                style = {'textAlign': 'center', 'margin': '20px'}
            ),
            html.Hr(),
            html.P("This website can find certifications that return general elective credits as well. To find"
                   " an elective credit search by the department code, the level of elective credit, and the "
                   "term ELE. For example, 100 level IT elective credits would be IT1ELE, 200 level "
                   "IT elective credits would be IT2ELE, and so on.",
                   style={'textAlign': 'center', 'margin': '20px'}
                   ),
            html.Div(
                [
                    html.Br(),
                    html.Label("Enter your course ID (EX101):"),
                    dcc.Input(id="course_id", type="text", value="", style = {"margin": "10px 10px"}),
                    html.Button("Submit", id="submit_button", n_clicks=0),
                ],
                style= {'textAlign': 'center', 'margin': '20px'}
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
    app.run(debug=False, use_reloader=True, port=80)

@app.callback(
    Output("output_div", "children"),
    [Input("submit_button", "n_clicks"),
     Input("course_id", "n_submit")],
    State("course_id", "value")
)

def update_output(n_clicks, n_submit, course_id):
    """
    Callback function to update the output based on the course ID input.
    :param n_clicks: Number of times the submit button has been clicked.
    :param course_id: The course ID entered by the user.
    :return: HTML content to display the course alternatives or an error message.
    """
    course_id.strip()  # Remove any leading or trailing whitespace
    if (n_clicks and n_clicks > 0) or (n_submit and n_submit > 0):
        if not course_id:
            return html.Div("Please enter a valid course ID.", style={'color': 'red', 'textAlign': 'center'})

        # Fetch alternatives for the given course ID
        alternatives = kd.load_courses().get(course_id)

        if not alternatives:
            return html.Div(f"No certifications found for {course_id}.", style={'color': 'red', 'textAlign': 'center'})

        alternatives = alternatives.Certifications

        if not alternatives:
            return html.Div(f"No certifications found for {course_id}.", style={'color': 'red'})

        data = [
            {"Title": cert.title.strip(), "Provider": cert.provider.strip()}
            for cert in alternatives
        ]

        return html.Div([
            html.H3(f"Certifications for {course_id}"),
            dash_table.DataTable(
                columns=[
                    {"name": "Provider", "id": "Provider"},
                    {"name": "Title", "id": "Title"}
                ],
                data=data,
                cell_selectable=False,
                style_table={'width': '100%', 'margin': 'auto', 'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '8px', 'minWidth': '100px', 'maxWidth': '300px', 'whiteSpace': 'normal'},
                style_header={'fontWeight': 'bold'}
            )
        ], style={'textAlign': 'center'})

    return html.Div("Enter a course ID and click Submit to see alternatives.", style={'textAlign': 'center'})

app.clientside_callback(
    """
    function(n_intervals) {
    var baseStyle = {'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'};
        if (window.innerWidth <= 600) {
            baseStyle['display'] = 'none';
        }
        return baseStyle;
    }
    """,
    Output("header_buttons", "style"),
    Input("resize-interval", "n_intervals"),
)


if __name__ == "__main__":
    os.environ["BROWSER"] = "none"  # Disable browser opening
    main()