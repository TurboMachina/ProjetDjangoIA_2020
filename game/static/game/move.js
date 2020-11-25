let board
let game_id
let errorMessage

window.onload = function() {
  board = document.getElementById("board").children[0]
  errorMessage = document.getElementById("error_message")
  document.getElementById("UP").addEventListener("click", movement({"move" : {"x" : -1, "y" : 0}}))
  document.getElementById("LEFT").addEventListener("click", movement({"move" : {"x" : 0, "y" : -1}}))
  document.getElementById("RIGHT").addEventListener("click", movement({"move" : {"x" : 0, "y" : 1}}))
  document.getElementById("DOWN").addEventListener("click", movement({"move" : {"x" : 1, "y" : 0}}))
  game_id = document.getElementById("game_id").innerText
}
function main(move) {
  const promise = jsonRPC("/game/move/" + game_id + "/", move);
  
  errorMessage.innerHTML = ""

  promise.then(result => loadBoard(JSON.parse(result)),
    (result) => errorMessage.innerHTML = result.errorMessage)
}
function movement(move) {
  return function() {
    main(move)
  }
}

function loadBoard(result) {
  let iColumn;
  let iLine = 0;
  result = JSON.parse(result)

  colors = ["black"]
  for (player of result._players) colors[player._userNumber] = player._color;

  for (line of board.children) {
    iColumn = 0

    for (column of line.children) {
      userNumber = result._gameState[iLine][iColumn]
      column.style.backgroundColor = colors[userNumber]
      column.classList.remove("actual_position")

      iColumn++
    }
    iLine++
  }

  if (result._winner) document.getElementById("winner").innerHTML = "winner is player " + result._winner

  document.getElementById("turn").innerHTML = "turn of player : " + result._turn 

  for (player of result._players) {
    board.children[player._posX].children[player._posY].classList.add("actual_position")
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
        resolve(xhr.response);
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