let board
let game_id
let errorMessage

window.onload = function() {
  board = document.getElementById("board").children[0]
  errorMessage = document.getElementById("error_message")
  document.getElementById("UP").addEventListener("click", movement({"move" : {"x" : 0, "y" : -1}}))
  document.getElementById("LEFT").addEventListener("click", movement({"move" : {"x" : -1, "y" : 0}}))
  document.getElementById("RIGHT").addEventListener("click", movement({"move" : {"x" : 1, "y" : 0}}))
  document.getElementById("DOWN").addEventListener("click", movement({"move" : {"x" : 0, "y" : 1}}))
  game_id = document.getElementById("game_id").innerText
}
function main(move) {
  const promise = jsonRPC("/game/move/" + game_id + "/", move);
  
  errorMessage.innerHTML = ""

  promise.then(result => {
    loadBoard(result)
  }).catch(result => {
    errorMessage.innerHTML = result.errorMessage
  })
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
      column.classList.remove("actual_position")

      iColumn++
    }
    iLine++
  }
  for (player in response.players) {
    board.children[player.posY].children[player.posX].classList.add("actual_position")
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
          errorMessage: JSON.parse(xhr.response).error_message
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