// scripts.js complet avec reset du labyrinthe + affichage du scoreboard + réduction taille labyrinthe

let playerCol = 0;
let playerRow = 0;
let playerMoving = false;

document.addEventListener("DOMContentLoaded", () => {
  const replayButton = document.querySelector(".button");
  const seedInput = document.querySelector("#seed");
  const gameDiv = document.querySelector(".gameDiv");
  const scoresDiv = document.querySelector(".scoresDiv");

  replayButton.addEventListener("click", async () => {
    let seed = seedInput.value;
    if (!seed) {
      seed = Math.floor(Math.random() * 10000000);
    }

    try {
      const response = await fetch(`https://green-escape.onrender.com/api/generate_maze?seed=${seed}`);
      const data = await response.json();

      const maze = data.maze;
      window.maze = maze;
      window.exit = data.exit;
      const [startX, startY] = data.entrance;

      gameDiv.innerHTML = ""; // Reset complet
      scoresDiv.style.display = "none";

      const container = document.createElement("div");
      container.style.display = "grid";
      container.style.gridTemplateColumns = `repeat(${maze[0].length}, 20px)`;
      container.style.gridAutoRows = "20px";
      container.style.position = "relative";
      container.style.margin = "0 auto";
      container.id = "maze-container";

      maze.forEach((row) => {
        row.forEach((cell) => {
          const cellDiv = document.createElement("div");
          const img = document.createElement("img");

          img.src = cell === 1 ? "../static/images/mur.png" : "../static/images/sol.png";
          img.style.width = "20px";
          img.style.height = "20px";

          cellDiv.appendChild(img);
          container.appendChild(cellDiv);
        });
      });

      const playerImg = document.createElement("img");
      playerImg.id = "player";
      playerImg.src = "../static/images/BackGuy.png";
      playerImg.style.width = "20px";
      playerImg.style.height = "20px";
      playerImg.style.position = "absolute";
      playerImg.style.zIndex = "10";

      const cellSize = 20;
      playerImg.style.left = `${startX * cellSize}px`;
      playerImg.style.top = `${startY * cellSize}px`;

      playerCol = startX;
      playerRow = startY;

      container.appendChild(playerImg);

      gameDiv.appendChild(container);

      window.algoScores = data.scores;
      window.playerStarted = false;
      window.startTime = null;
    } catch (error) {
      console.error("Erreur lors du fetch du labyrinthe :", error);
    }
  });
});

document.addEventListener("keydown", (e) => {
  e.preventDefault();
  if (playerMoving) return;

  const directionKeys = {
    ArrowUp: [0, -1, "BackGuy.png"],
    ArrowDown: [0, 1, "FrontGuy.png"],
    ArrowLeft: [-1, 0, "LeftGuy.png"],
    ArrowRight: [1, 0, "RightGuy.png"],
  };

  if (!(e.key in directionKeys)) return;
  const [dx, dy, sprite] = directionKeys[e.key];
  const player = document.getElementById("player");

  if (!player || !window.maze) return;

  const cellSize = 20;
  player.src = `../static/images/${sprite}`;

  if (!window.playerStarted) {
    window.startTime = Date.now();
    window.playerStarted = true;
  }

  playerMoving = true;

  function isIntersection(x, y) {
    const directions = [[0,1],[1,0],[0,-1],[-1,0]];
    let count = 0;
    for (const [dx, dy] of directions) {
      const nx = x + dx;
      const ny = y + dy;
      if (window.maze[ny]?.[nx] === 0) count++;
    }
    return count >= 3;
  }

  function afficherScoreboard(elapsed) {
    console.log(">>> afficherScoreboard appelé ! Temps :", elapsed);
    const scoresDiv = document.querySelector(".scoresDiv");
    const container = document.getElementById("maze-container");
    if (container) {
      container.style.margin = "0"; // haut gauche
      container.style.display = "grid";
      container.style.transform = "scale(0.6) translate(-20%, -20%)";
      container.style.transition = "transform 0.5s ease-in-out, margin 0.5s ease-in-out";
    }

    scoresDiv.innerHTML = "<h1>Scores</h1>";
    scoresDiv.style.display = "block";
    scoresDiv.style.visibility = "visible";
    scoresDiv.style.opacity = "1";
    scoresDiv.style.position = "relative";
    scoresDiv.style.zIndex = "5";

    if (window.algoScores) {
      window.algoScores.forEach(([algo, time], index) => {
        const entry = document.createElement("div");
        entry.classList.add("scoreEntry");

        const rank = document.createElement("span");
        rank.classList.add("rank");
        rank.textContent = `#${index + 1}`;

        const name = document.createElement("span");
        name.classList.add("algo");
        name.textContent = algo;

        const timing = document.createElement("span");
        timing.classList.add("time");
        timing.textContent = `${(time * 30000).toFixed(2)} s`;
        entry.appendChild(rank);
        entry.appendChild(name);
        entry.appendChild(timing);
        scoresDiv.appendChild(entry);
      });
    }
    let medails = 0;
    window.algoScores.forEach(([algo, time], index) => {
      if(elapsed < (time * 30000).toFixed(2)) {
        medails = medails + 1;
      }
      console.log("medails",medails);
    });
    fetch("https://green-escape.onrender.com/api/saveMedals", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // ← super important pour que Django voie l'utilisateur connecté
      body: JSON.stringify({ medals: medails }),
    });
    const playerEntry = document.createElement("div");
    playerEntry.classList.add("scoreEntry");

    const playerRank = document.createElement("span");
    playerRank.classList.add("rank");
    playerRank.textContent = "★";

    const playerName = document.createElement("span");
    playerName.classList.add("algo");
    playerName.textContent = "Player";

    const playerTime = document.createElement("span");
    playerTime.classList.add("time");
    playerTime.textContent = `${elapsed} s`;

    playerEntry.appendChild(playerRank);
    playerEntry.appendChild(playerName);
    playerEntry.appendChild(playerTime);
    scoresDiv.appendChild(playerEntry);
    
  }

  async function saveTime(seed,elapsed) {
    try {
      console.log(seed, elapsed);
      console.log(seed);
      const response = await fetch("/api/saveTime/", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json" ,
          },
          body: JSON.stringify({ seed , elapsed })
      });

      const result = await response.json();

      if (response.ok) {
          alert("bien ouej !")  // Redirige vers la page principale après connexion
      } else {
          document.getElementById("errorMessage").textContent = result.error;  // Affiche l'erreur si échec
      }
  } catch (error) {
      console.error("Erreur lors de la connexion :", error);
  }    
  }

  function moveUntilIntersection() {
    let interval = setInterval(() => {
      const nx = playerCol + dx;
      const ny = playerRow + dy;

      if (
        ny < 0 || ny >= window.maze.length ||
        nx < 0 || nx >= window.maze[0].length ||
        window.maze[ny][nx] === 1
      ) {
        clearInterval(interval);
        playerMoving = false;
        return;
      }

      playerCol = nx;
      playerRow = ny;

      player.style.left = `${playerCol * 20}px`;
      player.style.top = `${playerRow * 20}px`;

      const trail = document.createElement("div");
      trail.style.width = "20px";
      trail.style.height = "20px";
      trail.style.backgroundColor = "rgba(0, 255, 0, 0.3)";
      trail.style.position = "absolute";
      trail.style.left = `${playerCol * 20}px`;
      trail.style.top = `${playerRow * 20}px`;
      trail.style.zIndex = "5";
      document.getElementById("maze-container").appendChild(trail);

      if (playerCol === window.exit[0] && playerRow === window.exit[1]) {
        clearInterval(interval);
        playerMoving = false;

        const elapsed = ((Date.now() - window.startTime) / 1000).toFixed(2);
        afficherScoreboard(elapsed);
        saveTime(seed.value,elapsed)
        return;
      }

      if (isIntersection(playerCol, playerRow)) {
        clearInterval(interval);
        playerMoving = false;
      }
    }, 50);
  }

  moveUntilIntersection();
});