document.addEventListener("DOMContentLoaded", () => {
  const replayButton = document.querySelector(".button");
  const seedInput = document.querySelector("#seed");
  const gameDiv = document.querySelector(".gameDiv");
  const scoresDiv = document.querySelector(".scoresDiv");

  replayButton.addEventListener("click", async () => {
    // 1. Récupérer ou générer une seed
    let seed = seedInput.value;
    if (!seed) {
      seed = Math.floor(Math.random() * 10000000);
      console.log("Seed générée :", seed);
    } else {
      console.log("Seed utilisée :", seed);
    }

    try {
      // 2. Appel au backend Django
      const response = await fetch(`http://localhost:8000/api/generate_maze?seed=${seed}`);
      const data = await response.json();

      const maze = data.maze;
      console.log("Maze reçu :", maze);

      // 3. Réinitialiser l'affichage du labyrinthe
      gameDiv.innerHTML = "";

      // 4. Créer une grille dynamique pour le labyrinthe
      const container = document.createElement("div");
      container.style.display = "grid";
      container.style.gridTemplateColumns = `repeat(${maze[0].length}, 16px)`;
      container.style.gridAutoRows = "16px";
      container.style.gap = "0";
      container.style.margin = "0 auto";

      // 5. Remplir la grille avec des images pixel art
      maze.forEach(row => {
        row.forEach(cell => {
          const cellDiv = document.createElement("div");
          const img = document.createElement("img");

          img.src = cell === 1 ? "../images/mur.png" : "../images/sol.png";
          img.style.width = "20px";
          img.style.height = "20px";

          cellDiv.appendChild(img);
          container.appendChild(cellDiv);
        });
      });

      gameDiv.appendChild(container);

      // 6. Affichage des scores dans la div scoresDiv
      scoresDiv.innerHTML = "<h1>Scores</h1>";
      if (data.scores && data.scores.length > 0) {
        data.scores.forEach(([algo, time], index) => {
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
          timing.textContent = `${time.toFixed(5)*50000} s`;
        
          entry.appendChild(rank);
          entry.appendChild(name);
          entry.appendChild(timing);
          scoresDiv.appendChild(entry);
        });
        
      } else {
        scoresDiv.innerHTML += "<p>Aucun score reçu.</p>";
      }

    } catch (error) {
      console.error("Erreur lors du fetch du labyrinthe :", error);
    }
  });
});
