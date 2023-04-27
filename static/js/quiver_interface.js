var quiverUi = null;       // Global var holding ref to Quiver's ui singleton
var quiverHistory = null;
var quiverLoadDiagram = null;
var quiverIframe = null;
var csrfToken = null;
var saveDiagramURL = null;
var loadDiagramURL = null;
var diagramId = null;
var diagramName = null;
var renameDiagramURL = null;

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
    var data = JSON.stringify(data);

    return fetch(url,
    {
        headers: {
        'X-CSRFToken': csrfToken,
        "x-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json; charset=utf-8",
    },
    method: 'POST',
    body: data,
    mode: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        //alert("Success: " + JSON.stringify(data));
        display_django_messages();
        return data;
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

function rename_diagram()
{
    var text = $('#diagram-name-input').val();

    if (text != diagramName)
    {
        post_json_to_url(renameDiagramURL, text)
        .then(
            data => {
                if (data != null && 'success' in data)
                {
                    if (data['success'])
                    {
                        $('#diagram-name-close-button').trigger('click');
                        $('#diagram-name').text(text);
                        $('#diagram-name-input').val(text);
                        diagramName = text;
                    }
                    // else {
                    //     // $('#diagram-name-input').val(diagramName);
                    // }
                }
            });
    }
}
