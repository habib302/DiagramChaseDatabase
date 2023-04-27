var quiverUi = null;       // Global var holding ref to Quiver's ui singleton
var quiverHistory = null;
var quiverLoadDiagram = null;
var quiverIframe = null;
var csrfToken = null;
var saveDiagramURL = null;
var loadDiagramURL = null;

function save_diagram_to_database()
{
    var ui = quiverUi;
    var history = quiverHistory;
    const options = ui.options();
    const definitions = ui.definitions();

    const { data, meta_data, json_data } = ui.quiver.export(
        "json",
        ui.settings,
        options,
        definitions,
    );
    
    // `data` is the new URL.
    history.pushState({}, "", data);

    post_json_to_url(saveDiagramURL, json_data);
}

function post_json_to_url(url, data)
{
        // I couldn't get post_string_to_url to run without CSRF failure here.
    fetch(url, 
    {
        headers: {
        'X-CSRFToken': csrfToken,
        "x-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json; charset=utf-8",
    },
    method: 'POST',
    body: JSON.stringify(data),
    mode: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        //alert("Success: " + JSON.stringify(data));
        display_django_messages();
    })
    .catch(error => {
        alert(error);
        console.error('Error: ' + error);
    });
}

function load_diagram_from_database()
{
    get_json_from_url(loadDiagramURL)
    .then(response => {
        return response.text();
    })
    .then(data => {
        //alert(data);
        var iframeURL = $(quiverIframe).attr('src');
        const URL_prefix = iframeURL.replace(/\?.*$/, "");
        iframeURL = `${URL_prefix}?q=${btoa(unescape(encodeURIComponent(data)))}`;
        $(quiverIframe).attr('src', iframeURL);
        quiverLoadDiagram();
        hide_quiver_grid();
    });
}

function get_json_from_url(url)
{
    return fetch(url, 
    {
        headers: {
            'Accept': 'text/plain; charset=utf8',
            'X-Requested-With': 'XMLHttpRequest',   //Necessary to work with request.is_ajax()
        }
    });
}


