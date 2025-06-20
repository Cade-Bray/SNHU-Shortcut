from dash import html, Dash, dcc, dash_table, Input, Output, State, exceptions, callback_context
from dotenv import load_dotenv
import kuali_driver as kd
import base64
import flask
import time
import os
import re

#########################
# Dashboard Layout / View
#########################

# Load environment variables from .env file
load_dotenv()
ADSENSE_CLIENT_ID = os.getenv("ADSENSE_CLIENT_ID")

app = Dash(
        "SNHU Shortcut Dash App",
        assets_url_path="/.images",
        assets_folder=".images",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
            {"name": "google-adsense-account", "content": ADSENSE_CLIENT_ID}
        ],
    )

# Create a Dash application
app.title = "SNHU Shortcut"

# Load the logo image
logo_path = ".images/Logo.jpg"
with open(logo_path, "rb") as logo_file:
    logo_data = logo_file.read()
logo_encoded = base64.b64encode(logo_data).decode("utf-8")

app.layout = html.Div(
    children = [
        dcc.Location(id='url', refresh=False),
        html.Script(
            f'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}',
            crossOrigin = "anonymous",
            **{'async': True}
        ),
        html.Div(
            style= {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between',
                    'alignItems': 'center', 'padding': '10px', 'flexWrap': 'wrap', 'overflow': 'hidden'},
            children=[
                html.Div(
                    style = {'display': 'flex','flexDirection': 'row' , 'alignItems': 'center', 'position': 'relative'},
                    children = [
                        html.A(
                            href= "/",
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
                       " more cost effective way or to allow for more flexibility in their in their education. Some "
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
                    "certification page is structured in such a way that it is difficult to find certifications that"
                    " satisfy a specific course. This website allows you to enter a course ID and find all instantly"
                    ". Please note that this website is updating daily and may not have the most up to date depending "
                    "on the most recent update to the SNHU certifications page."
                ]),
                html.Br()
            ],
            style = {'textAlign': 'center', 'margin': '20px'}
        ),
        html.Hr(),
        html.P("This website can find certifications that return general elective credits as well. To find"
               " an elective credit search by the department code, the level of elective credit, and the "
               "term ELE. For example, 100 level GEN as in General elective credits would be GEN1ELE, 200 level "
               "IT elective credits would be IT2ELE, and so on. Partial searches are also supported by entering "
               "GEN1, IT2, or ELE. This will return all certifications that match the partial search.",
               style={'textAlign': 'center', 'margin': '20px'}
               ),
        html.Div(
            [
                html.Br(),
                html.Label("Enter your course ID:"),
                dcc.Input(id="course_id", type="text", value="", n_submit=0, placeholder="EX101",
                          style={"margin": "5px", "width": "80px", "fontSize": "12px", "padding": "2px"}),
                html.Button("Submit", id="submit_button", n_clicks=0),
                html.Img(
                    id="share-icon",
                    src=".images/share-icon.png",
                    title="Copy link to this search",
                    style={"height": "24px", "cursor": "pointer", "marginTop": "6px", "marginLeft": "10px"}
                ),
                html.Div(id="copy-feedback", style={"marginLeft": "10px", "color": "green"}),
                dcc.Store(id="copy-feedback-store", data="")
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
                html.A(href="mailto:bray.cade@gmail.com", target="_blank",
                       children=[
                           html.P("Contact@CadeBray.com")
                       ]
                )
            ],
            style = {'textAlign': 'center', 'margin': '20px'}
        )
    ]
)

def alphanum_key(s):
    # Split string into list of strings and integers
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

@app.callback(
    Output("output_div", "children"),
    Input("submit_button", "n_clicks"),
    Input("course_id", "n_submit"),
    Input("url", "pathname"),
    State("course_id", "value")
)
def update_output(n_clicks, n_submit, pathname, course_id):
    """
    Callback function to update the output based on the course ID input.
    :param n_clicks: Number of times the submit button has been clicked.
    :param n_submit: Number of times the course ID input has been submitted.
    :param course_id: The course ID entered by the user.
    :param pathname: The current URL path.
    :return: HTML content to display the course alternatives or an error message.
    """
    if pathname and pathname != "/":
        course_id = pathname.lstrip("/")
        n_clicks = 1  # Simulate a submit

    # Determine which input triggered the callback
    trigger = n_clicks or n_submit
    # Sanitize the course_id input
    course_id = kd.sanitize_input(course_id)

    # Log the request with timestamp and course ID. Print statements go to Passenger log.
    print(f"[INFO - {time.strftime('%Y-%m-%d %H:%M:%S')}] {flask.request.remote_addr} called: "
          f"course_id={'Homepage' if not course_id else course_id} by UI")

    # If no button has been clicked or submitted, return a default message
    if trigger and trigger > 0:
        # If course_id is empty, return an error message
        if not course_id:
            return html.Div("Please enter a valid course ID.", style={'color': 'red', 'textAlign': 'center'})

        # Fetch alternatives for the given course ID
        alternatives_root = kd.load_courses()
        alternatives = alternatives_root.get(course_id)

        if not alternatives:
            # If the course_id is not found in the loaded courses, return an error message
            if any(course_id in key for key in alternatives_root.keys()):
                # This assumes that the course_id is a partial match such as a department code or a course number.
                # Return a data table with Course ID, Title, and Provider
                data = []
                # Iterate through the alternatives_root to find matching course objects
                for key in alternatives_root.keys():
                    # Check if the course_id is a substring of the key
                    if course_id in key:
                        # If it is, extract the certifications for that course
                        for cert in alternatives_root[key].Certifications:
                            # Append the relevant data to the list
                            data.append({
                                "Provider": cert.provider.strip(),
                                "Title": cert.title.strip(),
                                "Course ID (Partial)": key
                            })
                return html.Div([
                    html.H3(f"Certifications for {course_id}"),
                    dash_table.DataTable(
                        columns=[
                            {"name": "Course ID (Partial)", "id": "Course ID (Partial)"},
                            {"name": "Provider", "id": "Provider"},
                            {"name": "Title", "id": "Title"}
                        ],
                        data= sorted(data, key=lambda x: alphanum_key(x["Course ID (Partial)"])),
                        cell_selectable=False,
                        style_table={'width': '100%', 'margin': 'auto', 'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '8px', 'minWidth': '100px', 'maxWidth': '300px',
                                    'whiteSpace': 'normal'},
                        style_header={'fontWeight': 'bold'}
                    )
                ], style={'textAlign': 'center'})

            else:
                return html.Div(f"No certifications found for {course_id}.",
                                style={'color': 'red', 'textAlign': 'center'})

        alternatives = alternatives.Certifications

        if not isinstance(alternatives, list) or not alternatives:
            return html.Div(f"No certifications found for {course_id}.", style={'color': 'red', 'textAlign': 'center'})

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

    # If no button has been clicked or submitted, return a default message
    return html.Div("Enter a course ID and click Submit to see alternatives.", style={'textAlign': 'center'})

@app.server.route("/api/course/<course_id>")
def get_course_info(course_id):
    """
    Flask route to get course information by course ID.
    :param course_id: The course ID to look up.
    :return: JSON response with course information or error message.
    """
    # Sanitize the course_id input
    course_id = kd.sanitize_input(course_id)

    # Log the request with timestamp and course ID
    print(f"[INFO - {time.strftime('%Y-%m-%d %H:%M:%S')}] {flask.request.remote_addr} called: course_id={course_id} by API")

    alternatives = kd.load_courses().get(course_id)

    if not alternatives:
        print(f"[ERROR - {time.strftime('%Y-%m-%d %H:%M:%S')}] {flask.request.remote_addr} called: course_id={course_id}"
              f" - No certifications found")
        return flask.jsonify({"error": f"No certifications found for {course_id}."}), 404

    alternatives = alternatives.Certifications

    if not isinstance(alternatives, list) or not alternatives:
        print(
            f"[ERROR - {time.strftime('%Y-%m-%d %H:%M:%S')}] {flask.request.remote_addr} called: course_id={course_id}"
            f" - No certifications found")
        return flask.jsonify({"error": f"No certifications found for {course_id}."}), 404

    data = [
        {"Title": cert.title.strip(), "Provider": cert.provider.strip()}
        for cert in alternatives
    ]

    return flask.jsonify(data)

@app.callback(
    Output("course_id", "value"),
    Input("url", "pathname")
)
def set_input_from_url(pathname):
    if pathname and pathname != "/":
        return pathname.lstrip("/")
    return ""

@app.callback(
    Output("url", "pathname"),
    [Input("submit_button", "n_clicks"), Input("course_id", "n_submit")],
    State("course_id", "value"),
    prevent_initial_call=True
)
def update_url(n_clicks, n_submit, course_id):
    if not course_id:
        raise exceptions.PreventUpdate
    return f"/{course_id.strip()}"

@app.callback(
    [
        Output("copy-feedback-store", "data"),
        Output("copy-feedback", "children"),
    ],
    [
        Input("share-icon", "n_clicks"),
        Input("submit_button", "n_clicks"),
        Input("course_id", "n_submit"),
        Input("course_id", "value"),
    ],
    State("url", "pathname"),
    prevent_initial_call=True
)
def handle_feedback(share_clicks, submit_clicks, n_submit, course_value, pathname):
    ctx = callback_context
    if not ctx.triggered:
        return "", ""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "share-icon" and share_clicks:
        if pathname:
            return "Link copied!", "Link copied!"
    # Clear feedback on any other input
    return "", ""

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

app.clientside_callback(
    """
    function(n_clicks, pathname) {
        if (window.dash_clientside && n_clicks && pathname) {
            const url = window.location.origin + pathname;
            navigator.clipboard.writeText(url);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("share-icon", "title"),  # Dummy output, not used
    Input("share-icon", "n_clicks"),
    State("url", "pathname"),
    prevent_initial_call=True
)

if __name__ == "__main__":
    os.environ["BROWSER"] = "none"  # Disable browser opening

    # The app.run is for development purposes only
    app.run(debug=True, use_reloader=False, port=80)