let loggedIn = false;
let apiVer = "v1.0";

/** checking if access code is presented */
function checkcode() {
    console.log("Checking access code...");
    let url_string = window.location.href;
    let url = new URL(url_string);
    let code = url.searchParams.get("access_token");
    let clear = url.searchParams.get("clear");
    if (clear == 'true') {
        localStorage.removeItem('access_token');
        console.log("cleared access_token");
    }
    if (typeof code != "undefined" && code != '' && code != null) {
        code = encodeURIComponent(code);
        console.log("overriding access_token = " + code);
        localStorage.setItem('access_token', code);
        $("#login_panel").remove();
        loggedIn = true;
    } else {
        let access_token = localStorage.getItem('access_token');
        if (access_token != null) {
            console.log("from local storage: access_token = " + access_token);
            $("#login_panel").remove();
            loggedIn = true;
        } else {
            $("#login_panel").siblings().remove();
        }
    }
}

/** creating post */
function create_gist() {
    // read form data
    let content = $("#gist_content").val();
    let description = $("#gist_desc").val();
    let filename = $("#gist_filename").val();

    let access_token = readAccessToken();
    console.log("description=" + description + "\n" + "filename=" + filename + "\n" +
        "content=" + content);

    // send request to create gist
    if (content.trim()) {
        $.ajax({
            url: "/" + apiVer + "/gist",
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                "gist_description": description.trim(),
                "gist_filename": filename.trim(),
                "gist_content": content.trim()
            }),
            headers: {
                "access-token": access_token
            },
            success: function(result) {
                if (result.error != null) {
                    error(result.error);
                } else {
                    reload_gists();
                }
            }
        });
    } else {
        error("Please fill in the form.");
        console.log("Content is empty.");
    }
}

/** deleting a gist */
function delete_gist(gist_id) {
    let access_token = readAccessToken();

    // send request to delete gist
    $.ajax({
        url: "/" + apiVer + "/gist/" + gist_id,
        type: 'DELETE',
        dataType: 'json',
        headers: {
            "access-token": access_token
        },
        success: function(result) {
            if (result.error != null) {
                error(result.error);
            } else {
                reload_gists();
            }
        }
    });
}

/** listing gists */
function list_gists() {
    if (!loggedIn) {
        return;
    }
    console.log("Reading gists from github");

    let access_token = readAccessToken();

    $.ajax({
        url: "/" + apiVer + "/gist",
        type: 'GET',
        dataType: 'json',
        headers: {
            "access-token": access_token
        },
        success: function(result) {
            if (result.error != null) {
                error(result.error);
            } else {
                $("#gists_list").empty();
                let json_array = $.parseJSON(result);
                $.each(json_array, function(i, json) {
                    populate_gists(json);
                });
            }
        }
    });
}

/** populate gists */
function populate_gists(json) {
    let div = $("<div id='panel_" + json.id + "' class='gist_row'>"); {
        let li = $("<li class='right'>");
        li.html('<button type="button" class="btn btn-danger" onclick="delete_gist(\'' +
            json.id + '\')">DEL</button>');
        div.append(li);
    } {

        let li = $("<li>");
        let secret = json.public ? "" : " <span style='color:red'>[secret]</span>";
        li.html("<a href='" + json.html_url + "' target='_blank'>ID: " +
            json.id + secret + "</a>");
        div.append(li);
    } {
        let li = $("<li class='indent'>");
        li.html(json.description);
        div.append(li);
    } {
        let owner = json.owner;
        $("#owner").text(owner.login);
        let html_url = owner.html_url;
        let avatar_url = owner.avatar_url;
        let li = $("<li style='line-height:16px;'>");
        li.html("<a href='" + html_url + "' target='_blank'> " +
            "<img src='" + avatar_url + "' border='0' /></a> " +
            "Created at: " + json.created_at);
        div.append(li);
    } {
        let li = $("<li class='indent'>");
        let link = $("<a id='commentcount_" + json.id + "' href='javascript:void(0);''>");
        link.text("comments(" + json.comments + ")");
        li.append(link);
        link.click(function() {
            toggleComment(json.id);
        });
        div.append(li);

        let commentDiv = $("<div id='comment_" + json.id + "' class='indent hidden'>");
        if (json.comments == 0) {
            commentDiv.prepend("<div class='comment_row'>No comment yet. Leave a commment?</div>");
        }
        div.append(commentDiv);


        let commentArea = $("<textarea id='commentarea_" + json.id + "' class='comment hidden'>");
        commentDiv.append(commentArea);

        let commentBtn = $('<div><button type="button" class="btn btn-primary" ' +
            'onclick="create_comment(\'' + json.id + '\')"' +
            '>Comment</button></div>');
        commentDiv.append(commentBtn);
    }
    $("#gists_list").append(div);
}

/** creating comment */
function create_comment(gist_id) {
    let comment = $("#commentarea_" + gist_id).val();
    let access_token = readAccessToken();
    console.log("comment=" + comment);
    if (comment.trim()) {
        $.ajax({
            url: "/" + apiVer + "/gist/" + gist_id + "/comments",
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                "gist_comment": comment.trim()
            }),
            headers: {
                "access-token": access_token
            },
            success: function(result) {
                if (result.error != null) {
                    error(result.error);
                } else {
                    reload_comments(gist_id);
                }
            }
        });
    } else {
        console.log("Content is empty.");
    }
}

/** deleting a comment */
function delete_comment(gist_id, comment_id) {
    let access_token = readAccessToken();

    // send request to delete gist
    $.ajax({
        url: "/" + apiVer + "/gist/" + gist_id + "/comments/" + comment_id,
        type: 'DELETE',
        dataType: 'json',
        headers: {
            "access-token": access_token
        },
        success: function(result) {
            if (result.error != null) {
                error(result.error);
            } else {
                reload_comments(gist_id);
            }
        }
    });
}

/** listing gists */
function list_comments(gist_id) {
    if (!loggedIn) {
        return;
    }
    let comment_panel = $("#comment_" + gist_id);
    console.log("Reading comments of " + gist_id + " from github");
    let access_token = readAccessToken();
    $.ajax({
        url: "/" + apiVer + "/gist/" + gist_id + "/comments",
        type: 'GET',
        dataType: 'json',
        headers: {
            "access-token": access_token
        },
        success: function(result) {
            if (result.error != null) {
                error(result.error);
            } else {
                let json_array = $.parseJSON(result);
                comment_panel.find(".comment_row").remove();
                // update comment count
                $("#commentcount_" + gist_id).text("Comments(" + json_array.length + ")");
                if (json_array.length > 0) {
                    $.each(json_array, function(i, json) {
                        populate_comments(gist_id, json);
                    });
                } else {
                    comment_panel.prepend("<div class='comment_row'>No comment yet. Leave a commment?</div>");
                }
            }
        }
    });
}

/** populate comments */
function populate_comments(gist_id, json) {
    let comment_panel = $("#comment_" + gist_id);
    let div = $("<div id='panel_" + json.id + "' class='indent comment_row'>"); {
        let li = $("<li class='right'>");
        li.html('<a href="javascript:delete_comment(\'' +
            gist_id + '\', \'' + json.id + '\')">DEL</a>');
        div.append(li);
    } {
        let li = $("<li>");
        li.html(json.body);
        div.append(li);
    } {
        let user = json.user;
        let html_url = user.html_url;
        let avatar_url = user.avatar_url;
        let li = $("<li style='line-height:16px;'>");
        li.html("<a href='" + html_url + "' target='_blank'> " +
            "<img src='" + avatar_url + "' border='0' /></a> " +
            "Created at: " + json.created_at);
        div.append(li);
    }
    comment_panel.prepend(div);
}

function reload_gists() {
    list_gists();
}

function reload_comments(gist_id) {
    list_comments(gist_id);
}

/** toggle comment panel */
function toggleComment(gist_id) {
    let comment_panel = $("#comment_" + gist_id);
    let comment_area = $("#commentarea_" + gist_id);
    comment_panel.toggle();
    comment_area.toggle();
    let isVisible = comment_panel.is(':visible');
    console.log(comment_panel.is(':visible'));
    if (isVisible) {
        reload_comments(gist_id);
    }
}

/** reading access token from local storage */
function readAccessToken() {
    let access_token = localStorage.getItem('access_token');
    return access_token;
}

function loading_open() {
    $("#loading_panel").fadeIn(300);
}

function loading_close() {
    $("#loading_panel").fadeOut(300);
}

function error(message) {
    $.notify({
        // options
        message: message
    }, {
        // settings
        element: 'body',
        allow_dismiss: true,
        type: 'danger',
        placement: {
            from: "top",
            align: "center"
        },
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        },
    });
}

$(document).ajaxSend(function() {
    loading_open();
});

$(document).ajaxComplete(function() {
    loading_close();
});

$(document).ready(function() {
    checkcode();
    list_gists();
});
