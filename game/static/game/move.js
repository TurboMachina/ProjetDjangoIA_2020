window.onload = function() {
    document.getElementById("my_button").addEventListener("click", () => {
        main();
    });
}
async function main() {
    const response = await jsonRPC("/game/move", {game_id: "1", player_id: "42", move: [1, 0]});
    document.getElementById("my_board").textContent = JSON.stringify(response.board)
    colorChangeBoard()
}

function colorChangeBoard() {
  board = document.getElementById("board").children[0]
  let iColumn;
  let iLine = 0;

  for (line of board.children) {
    iColumn = 0

    for (column of line.children) {
      
      playerNum = response.board[iLine][iColumn]
      column.textContent = playerNum
      
      if (playerNum != 0)
        column.style.backgroundColor = response.players[playerNum - 1].color
      else 
        column.style.backgroundColor = "black"
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