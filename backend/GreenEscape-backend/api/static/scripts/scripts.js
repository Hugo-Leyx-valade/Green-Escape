// ✅ VERSION FINALE DE scripts.js corrigé avec :
// - champ seed fonctionnel (saisie clavier + suppression)
// - pseudo affiché correctement
// - pas de conflit DOMContentLoaded
// - game proprement initialisée

let playerCol = 0;
let playerRow = 0;
let playerMoving = false;
let username = "Player"; // Valeur par défaut

// Récupération pseudo AVANT tout
(async () => {
  try {
    const response = await fetch("/api/data-profile/");
    const user = await response.json();
    username = user.username || "Player";
  } catch (error) {
    console.error("Erreur profil :", error);
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  const gameDiv = document.querySelector(".gameDiv");
  const replayButton = document.querySelector(".button");
  const seedInput = document.querySelector("#seed");
  const scoresDiv = document.querySelector(".scoresDiv");

  // Ajout d'un message de bienvenue au chargement
  const welcomeDiv = document.createElement("div");
  welcomeDiv.id = "welcome";
  welcomeDiv.innerHTML = `
    <h1>Welcome in Green Escape !</h1>
    <h2>Will you be faster than the algorithms? Dive into the maze and prove it!</h2>
    <img src="/static/images/FrontGuy.png" alt="Avatar" style="width:60px;height:60px;margin-top:10px;">
  `;
  welcomeDiv.style.textAlign = "center";
  welcomeDiv.style.marginTop = "20px";
  gameDiv.appendChild(welcomeDiv);

  replayButton.addEventListener("click", async () => {
    // Supprimer le message de bienvenue dès qu'on clique sur Play
    const oldWelcome = document.getElementById("welcome");
    if (oldWelcome) oldWelcome.remove();

    let seed = seedInput.value.trim();
    if (seed && !/^[0-9]+$/.test(seed)) {
      alert("Please enter a numeric seed.");
      return;
    }
    if (!seed) seed = Math.floor(Math.random() * 10000000);

    try {
      const res = await fetch(`/api/generate_maze?seed=${seed}`);
      const data = await res.json();
      const maze = data.maze;
      const [startX, startY] = data.entrance;
      window.maze = maze;
      window.exit = data.exit;
      window.algoScores = data.scores;
      window.playerStarted = false;
      window.startTime = null;

      const old = document.getElementById("maze-container");
      if (old) old.remove();
      scoresDiv.style.display = "none";

      const container = document.createElement("div");
      container.id = "maze-container";
      container.style.display = "grid";
      container.style.gridTemplateColumns = `repeat(${maze[0].length}, 20px)`;
      container.style.gridAutoRows = "20px";
      container.style.position = "relative";
      container.style.margin = "0 auto";

      maze.forEach(row => row.forEach(cell => {
        const div = document.createElement("div");
        const img = document.createElement("img");
        img.src = cell === 1 ? "/static/images/mur.png" : "/static/images/sol.png";
        img.style.width = "20px";
        img.style.height = "20px";  
        div.appendChild(img);
        container.appendChild(div);
      }));

      const player = document.createElement("img");
      player.id = "player";
      player.src = "/static/images/BackGuy.png";
      player.style = `width: 20px; height: 20px; position: absolute; z-index: 10;`;
      player.style.left = `${startX * 20}px`;
      player.style.top = `${startY * 20}px`;

      playerCol = startX;
      playerRow = startY;

      container.appendChild(player);
      gameDiv.appendChild(container);
    } catch (e) {
      console.error("Erreur fetch maze:", e);
    }
  });
});

document.addEventListener("keydown", (e) => {
  const validKeys = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];

  if (!validKeys.includes(e.key)) {
      // Ce n'est pas une touche de direction, donc on ne bloque pas du tout
      return;
  }

  if (document.activeElement.tagName === "INPUT") {
      // Si on est dans un input, on ne fait rien non plus
      return;
  }
  e.preventDefault();
  if (playerMoving) return;

  const sprites = {
    ArrowUp: [0, -1, "BackGuy.png"],
    ArrowDown: [0, 1, "FrontGuy.png"],
    ArrowLeft: [-1, 0, "LeftGuy.png"],
    ArrowRight: [1, 0, "RightGuy.png"]
  };
  const [dx, dy, sprite] = sprites[e.key];
  const player = document.getElementById("player");
  if (!player || !window.maze) return;
  player.src = `/static/images/${sprite}`;

  if (!window.playerStarted) {
    window.startTime = Date.now();
    window.playerStarted = true;
  }
  playerMoving = true;

  const isIntersection = (x, y) => [[0,1],[1,0],[0,-1],[-1,0]].reduce((c, [dx,dy]) => c + (window.maze[y+dy]?.[x+dx] === 0 ? 1 : 0), 0) >= 3;

  const afficherScoreboard = async (elapsed) => {
    const scoresDiv = document.querySelector(".scoresDiv");
    const container = document.getElementById("maze-container");
    if (container) {
        container.style.margin = "0";
        container.style.transform = "scale(0.6) translate(-20%, -20%)";
        container.style.transition = "transform 0.5s ease-in-out";
    }

    scoresDiv.innerHTML = "<h1>Scores</h1>";
    scoresDiv.style.display = "block";

    const allScores = [...(window.algoScores || []).map(([algo, t]) => ({ name: algo, time: t * 25000, isPlayer: false })), 
                       { name: username, time: parseFloat(elapsed), isPlayer: true }];
    allScores.sort((a, b) => a.time - b.time);

    let algosBeaten = 0;
    allScores.forEach((entry, i) => {
        const div = document.createElement("div");
        div.className = "scoreEntry";
        div.innerHTML = `
            <span class="rank">${entry.isPlayer ? "⭐" : `#${i + 1}`}</span>
            <span class="algo">${entry.name}</span>
            <span class="time">${entry.time.toFixed(2)} s</span>
        `;
        scoresDiv.appendChild(div);

        // Compter les algorithmes battus
        if (!entry.isPlayer && entry.time > parseFloat(elapsed)) {
            algosBeaten++;
        }
    });

    // Mettre à jour les statistiques du joueur
    try {
        const response = await fetch("/api/update-stats/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute("content"),
            },
            body: JSON.stringify({ medails: algosBeaten }),
        });

        if (!response.ok) {
            console.error("Erreur lors de la mise à jour des stats :", await response.json());
        }
    } catch (error) {
        console.error("Erreur lors de la mise à jour des stats :", error);
    }
  };

  const interval = setInterval(() => {
    const nx = playerCol + dx;
    const ny = playerRow + dy;
    if (ny < 0 || ny >= window.maze.length || nx < 0 || nx >= window.maze[0].length || window.maze[ny][nx] === 1) {
      clearInterval(interval); playerMoving = false; return;
    }
    playerCol = nx; playerRow = ny;
    player.style.left = `${playerCol * 20}px`;
    player.style.top = `${playerRow * 20}px`;

    const trail = document.createElement("div");
    trail.style = `width:20px;height:20px;background:rgba(0,255,0,0.3);position:absolute;left:${playerCol * 20}px;top:${playerRow * 20}px;z-index:5`;
    document.getElementById("maze-container").appendChild(trail);

    if (playerCol === window.exit[0] && playerRow === window.exit[1]) {
      clearInterval(interval); playerMoving = false;
      const elapsed = ((Date.now() - window.startTime) / 1000).toFixed(2);
      afficherScoreboard(elapsed);
      return;
    }
    if (isIntersection(playerCol, playerRow)) {
      clearInterval(interval); playerMoving = false;
    }
  }, 50);
});