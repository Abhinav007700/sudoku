document.addEventListener("keydown", startGame);
    function startGame() {
        var startScreen = document.getElementById("startScreen");
        var gameScreen = document.getElementById("gameScreen");
        startScreen.style.display = "none";
        gameScreen.style.display = "block";
        
        const buttons = document.querySelectorAll(".number-button");
        buttons.forEach(button => {
            button.disabled = false;
        });
        var mistake=0;
        var row_no, col_no;
        // Remove the event listener after the first key press if needed
        document.removeEventListener("keydown", startGame);
        fetch('/get_solution_matrix')
        .then(response => response.json())
        .then(data => {
            var solved_board = data.solved_board;
            // For each cell
            const cells = document.querySelectorAll(".sudoku-cell");
            console.log(cells);
            cells.forEach(cell => {
                cell.addEventListener("click", function () {
                    // Remove "selected" class from all cells
                    const value = this.textContent;
                    if (value===""){
                        cells.forEach(cell => {
                            cell.classList.remove("selected");
                        });
                
                        // Add "selected" class to the clicked cell
                        this.classList.add("selected");
                
                        row_no = this.parentNode.parentNode.rowIndex; // Get the row index of the parent <tr>
                        col_no = this.parentNode.cellIndex; // Get the column index within the <tr>
                    }
                });
            });
            buttons.forEach(button => {
                button.addEventListener("click", function () {
                    const b_value=this.textContent;
                    if (b_value==solved_board[row_no][col_no]){
                        cells[row_no * 9 + col_no].textContent=solved_board[row_no][col_no];
                        cells[row_no * 9 + col_no].style.color="rgb(208, 0, 255)";

                        const allFilled = [...cells].every(cell => cell.textContent !== "");
                        if (allFilled) {
                            // Game over condition: Display game over message
                            alert("Congratulations! You completed the Sudoku puzzle.");
                            location.reload(); // Reload the page to restart the game
                        } 
                    }
                    else{
                        mistake+=1;
                        if (mistake>=3){
                            alert("Game Over! You made 3 mistakes.");
                            location.reload();
                        }
                    }
                });
            });
        })
        .catch(error => console.error('Error:', error));
    }

