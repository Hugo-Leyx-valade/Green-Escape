document.addEventListener("DOMContentLoaded", () => {
    const replayButton = document.querySelector(".button");
    const seedInput = document.querySelector("#seed");
    const gameDiv = document.querySelector(".gameDiv");
  
    replayButton.addEventListener("click", async () => {
      // Récupérer la seed
      let seed = seedInput.value;
      if (!seed) {
        seed = Math.floor(Math.random() * 10000000);
        console.log("Seed générée :", seed);
      } else {
        console.log("Seed utilisée :", seed);
      }
  
      try {
        // Appel au backend Django
        const response = await fetch(`http://localhost:8000/api/generate_maze?seed=${seed}`);
        const data = await response.json();
  
        const maze = data.maze;
        console.log("Maze reçu :", maze);
  
        // Réinitialiser l'affichage du labyrinthe
        gameDiv.innerHTML = "";
  
        // Créer une grille dynamique
        const container = document.createElement("div");
        container.style.display = "grid";
        container.style.gridTemplateColumns = `repeat(${maze[0].length}, 16px)`;
        container.style.gridAutoRows = "16px";
        container.style.gap = "0";
        container.style.margin = "0 auto";
  
        // Générer chaque cellule avec une image
        maze.forEach(row => {
          row.forEach(cell => {
            const cellDiv = document.createElement("div");
            const img = document.createElement("img");
  
            if (cell === 1) {
              img.src = "../images/mur.png";
            } else {
              img.src = "../images/sol.png";
            }
  
            img.style.width = "20px";
            img.style.height = "20px";
            cellDiv.appendChild(img);
            container.appendChild(cellDiv);
          });
        });
  
        gameDiv.appendChild(container);
      } catch (error) {
        console.error("Erreur lors du fetch du labyrinthe :", error);
      }
    });
  });
  