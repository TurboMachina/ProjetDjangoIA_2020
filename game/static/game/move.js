let board
let game_id

window.onload = function() {
  board = document.getElementById("board").children[0]
  document.getElementById("UP").addEventListener("click", movement({"move" : {"x" : 0, "y" : -1}}))
  document.getElementById("LEFT").addEventListener("click", movement({"move" : {"x" : -1, "y" : 0}}))
  document.getElementById("RIGHT").addEventListener("click", movement({"move" : {"x" : 1, "y" : 0}}))
  document.getElementById("DOWN").addEventListener("click", movement({"move" : {"x" : 0, "y" : 1}}))
  game_id = document.getElementById("game_id").innerText
}
async function main(move) {
    const response = await jsonRPC("/game/move/" + game_id + "/", move);
    console.log(response)
    document.getElementById("my_board").textContent = JSON.stringify(response.gameState)
    loadBoard(response)
}

function movement(move) {
  return function() {
    main(move)
  }
}

function loadBoard(response) {
  let iColumn;
  let iLine = 0;

  color = ["black"]
  for (player in response.players) color[player.playerNum] = player.color.toString(16);

  for (line of board.children) {
    iColumn = 0

    for (column of line.children) {
      
      playerNum = response.gameState[iLine][iColumn]
      column.textContent = playerNum
      column.style.backgroundColor = color[playerNum]

      iColumn++
    }
    iLine++
  }
}

function jsonRPC(url, data) {
    return new Promise(function (resolve, reject) {
      let xhr = new XMLHttpRequest();
      xhr.open("POST", url);
      xhr.setRequestHeader("Content-type", "application/json");
      const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]")
        .value;
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.onload = function () {
        if (this.status >= 200 && this.status < 300) {
          resolve(JSON.parse(xhr.response));
        } else {
          reject({
            status: this.status,
            statusText: xhr.statusText,
          });
        }
      };
      xhr.onerror = function () {
        reject({
          status: this.status,
          statusText: xhr.statusText,
        });
      };
      xhr.send(JSON.stringify(data));
    });
}