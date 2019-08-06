window.onload = function() {
    createCommands();
}

function removeUselessLines(commands) {
    // remove empty lines and lines that start with #
    lines = commands.split("\n")
    out = ""
    for (i = 0; i < lines.length; i++) {
        if (lines[i].startsWith("#"))
            continue;
        out += lines[i] + "\n";
    }
    return out;
}

function replaceGroupLines(commands) {
    // replaces lines that start with "GROUP" with modifyNames or modifyTags commands
    modifyNames = document.getElementById("modifyNames").checked
    modifyTags = document.getElementById("modifyTags").checked

    lines = commands.split("\n")
    out = ""
    for (i = 0; i < lines.length; i++) {
        if (lines[i].startsWith("GROUP: ")) {
            name = lines[i].replace("GROUP: ", "").trim();
            lines[i] = "\n";
            if (modifyNames)
                lines[i] += `modifyNames "${name}"; `;
            if (modifyTags)
                lines[i] += `modifyTags "${name}"; `;
        }
        out += lines[i] + "\n";
    }
    return out;
}

function replaceAbfLines(commands) {
    // replace lines that start with "ABF" with setpath then a custom command
    analysisCommand = document.getElementById("customCommand").value;
    protocolMatch = document.getElementById("protocolList").value;
    lines = commands.split("\n")
    out = ""
    for (i = 0; i < lines.length; i++) {
        if (lines[i].startsWith("ABF: ")) {
            line = lines[i].replace("ABF: ", "").trim().split(", ");
            abf = line[0];
            protocol = line[1];
            comments = line[2];
            if (protocol.includes(protocolMatch)) {
                out += `setpath "${abf}"; ${analysisCommand}\n`;
            }
        } else {
            out += lines[i] + "\n";
        }
    }
    return out;
}

function populateProtocolList(commands) {
    // make the combobox show all protocols

    lines = commands.split("\n")
    var protocols = [];
    var protocolList = document.getElementById("protocolList");

    if (protocolList.options.length)
        return;

    for (i = 0; i < lines.length; i++) {
        if (lines[i].startsWith("ABF: ")) {
            line = lines[i].replace("ABF: ", "").trim().split(", ");
            abf = line[0];
            protocol = line[1].replace(",", "").trim();
            comments = line[2];
            if (!protocols.includes(protocol)) {
                protocols.push(protocol);
                var option = document.createElement("option");
                option.text = protocol;
                protocolList.add(option);
            }
        }
    }
}

function cmdAdd(command) {

    if (command == "clear")
        document.getElementById("customCommand").value = "";
    else
        document.getElementById("customCommand").value = document.getElementById("customCommand").value + command + "; ";
}

function createCommands() {

    //document.getElementById("cellListBlock").style.visibility = "collapse";
    //document.getElementById("originCommandBlock").style.visibility = "collapse";


    commands = document.getElementById("cellList").innerHTML
    populateProtocolList(commands);
    commands = removeUselessLines(commands)
    commands = replaceGroupLines(commands)
    commands = replaceAbfLines(commands)
    commands = commands.trim();
    document.getElementById("originCommands").innerHTML = commands;
}