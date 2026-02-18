import time
import random
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_txt_file(filename):
    try:
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' tidak ditemukan.")
            sys.exit()
            
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if not lines:
            print("Error: File kosong.")
            sys.exit()
        if lines[0].isdigit():
            n = int(lines[0])
            board_data = lines[1:]
        else:
            n = len(lines)
            board_data = lines

        board = []
        for line in board_data:
            if len(line) != n:
                print(f"Error: Panjang baris '{line}' ({len(line)}) tidak sesuai dengan N ({n}).")
                sys.exit()
            board.append(list(line))
            
        return n, board
    except Exception as e:
        print(f"Gagal membaca file .txt: {e}")
        sys.exit()
def image_to_board(image_path, N):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: File '{image_path}' tidak ditemukan.")
        sys.exit()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    cell_h = h / N
    cell_w = w / N
    
    board = []
    color_map = {}  
    next_char = 65 
    
    print(f"Dimensi Gambar: {w}x{h}, Estimasi per kotak: {cell_w:.2f}x{cell_h:.2f} px")

    for r in range(N):
        row_chars = []
        for c in range(N):
            cy = int(r * cell_h + cell_h / 2)
            cx = int(c * cell_w + cell_w / 2)
            cy = min(cy, h - 1)
            cx = min(cx, w - 1)
            pixel_color = img[cy, cx]
            
            found_char = None
            for key_color, char in color_map.items():
                diff_r = int(pixel_color[0]) - int(key_color[0])
                diff_g = int(pixel_color[1]) - int(key_color[1])
                diff_b = int(pixel_color[2]) - int(key_color[2])
                dist = np.sqrt(diff_r**2 + diff_g**2 + diff_b**2)
                
                if dist < 45:
                    found_char = char
                    break
            if found_char is None:
                found_char = chr(next_char)
                color_map[tuple(pixel_color)] = found_char
                next_char += 1
                if next_char > 90: next_char = 97
            
            row_chars.append(found_char)
        board.append(row_chars)
        
    return board

def save_solution_image(board, queens, N, filename):
    cell_size = 60
    img_size = N * cell_size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)
        
    unique_chars = set(cell for row in board for cell in row)
    palette = {char: (random.randint(100, 230), random.randint(100, 230), random.randint(100, 230)) for char in unique_chars}
    font = ImageFont.truetype("arial.ttf", 30)


    for r in range(N):
        for c in range(N):
            char = board[r][c]
            color = palette.get(char, (200, 200, 200))
                
            x0 = c * cell_size
            y0 = r * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
                
            draw.rectangle([x0, y0, x1, y1], fill=color, outline="black")
            is_queen = False
            for q in queens:
                if q[0] == r and q[1] == c:
                    is_queen = True
                    break
                
            if is_queen:
                draw.ellipse([x0+10, y0+10, x1-10, y1-10], fill="black")
                draw.text((x0+20, y0+15), "Q", fill="white", font=font)
        
    img.save(filename)
    print(f"Gambar berhasil disimpan ke: {filename}")


def verify(board, queens, sectors, curX, curY):
    for queen in queens :
        if abs(queen[0] - curX) <= 1 and abs(queen[1] - curY) <= 1:
            return False
        if queen[0] == curX or queen[1] == curY:
            return False
    for sector in sectors :
        if board[curX][curY] == sector[0] and sector[1] == True :
            return False
    return True

def add(x):
    return x+1

def addQueens(board, queens, sectors, alt, curX, curY):
    alt[0] = add(alt[0])
    x = board[curX][curY]
    queens.append([curX, curY, x])
    for i in range(len(sectors)):
        if sectors[i][0] == x:
            sectors[i][1] = True
            break

def removeQueens(queens, sectors):
    lastQueen = queens.pop()
    sectorLetter = lastQueen[2]
    for sector in sectors:
        if sector[0] == sectorLetter:
            sector[1] = False
            break

def finalBoard(board, queens, numQueens):
    newBoard = [[None for _ in range(numQueens)] for _ in range(numQueens)]
    for i in range(numQueens):
        for j in range(numQueens):
            if any(q[0] == i and q[1] == j for q in queens):
                newBoard[i][j] = '#'
            else:
                newBoard[i][j] = board[i][j]
    return newBoard
def makeSector(board, sectors):
    seen = set()
    for row in board:
        for cell in row:
            if cell not in sectors:
                sectors.append([cell, False])
                seen.add(cell)
    return sectors
def printBoard(board):
    for row in board:
        print(' '.join(row))

def print_live_board(board, queens, n, cases):
    sys.stdout.write("\033[H") 
    print(f"=== LIVE UPDATE (Iterasi: {cases}) ===")
    for r in range(n):
        row_str = ""
        for c in range(n):
            is_q = any(q[0] == r and q[1] == c for q in queens)
            row_str += "# " if is_q else ". "
        print(row_str)

def helperChecker(board, queens, sectors, found, alt, curX, curY, numQueens, show_live, interval):
    if curX >= numQueens:
        return
    while (curX < numQueens) and (not (verify(board, queens, sectors, curX, curY))):
        curY += 1
        if curY >= numQueens :
            curY = 0
            curX += 1
    if curX >= numQueens:
        return
    addQueens(board, queens, sectors, alt, curX, curY)
    if show_live and alt[0] % interval == 0:
        print_live_board(board, queens, n, alt[0])
    if numQueens == len(queens):
        found[0] = True
    if not(found[0]):
        helperChecker(board, queens, sectors, found, alt, curX, curY, numQueens, show_live, interval)
    else:
        return
    if not(found[0]):
        removeQueens(queens, sectors)
        curY += 1
        if curY >= numQueens :
            curY = 0
            curX += 1
        helperChecker(board, queens, sectors, found, alt, curX, curY, numQueens, show_live, interval)
    else:
        return
print("=== Program Tugas Kecil 1 ===")
print("Pilih metode input:")
print("1. Manual (Ketik teks / Copy-Paste)")
print("2. Input Gambar (File .png / .jpg)")
print("3. Input TXT (File .txt)")
pilihan = input("Masukkan pilihan (1/2/3): ")

board = []
queens = []
sectors = []
found = [False]
alt = [0]
if pilihan == "1":
    n = int(input("Masukkan ukuran board: "))
    print("Masukkan board:")
    for i in range(n):
        row = input().strip()
        board.append(list(row))
elif pilihan == '2':
    path = input("Masukkan nama lokasi file gambar (contoh: test.png): ")
    try:
        val_n = input("Masukkan ukuran N: ")
        n = int(val_n)
            
        print("\nSedang memproses gambar...")
        board = image_to_board(path, n)
            
        print("\n--- Board ---")
        printBoard(board)
        print("------------------------\n")
            
    except ValueError:
        print("Input ukuran harus angka.")
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
elif pilihan == '3':
    path = input("Masukkan nama lokasi file .txt (contoh: soal.txt): ")
    n, board = read_txt_file(path)
    print(f"\nBerhasil membaca file. N = {n}")
    print("--- Board dari File ---")
    printBoard(board)
    print("-----------------------\n")

show_live = True
interval = 10000
clear_screen()
makeSector(board, sectors)
start_time = time.time()
helperChecker(board, queens, sectors, found, alt, 0, 0, n, show_live, interval)
end_time = time.time()
duration = (end_time - start_time) * 1000
FinalBoard = finalBoard(board, queens, n)
printBoard(FinalBoard)
print(f"Jumlah Kasus yang ditinjau : {alt[0]}")
print(f"Duration time : {duration:.2f} ms")
save = str(input("Apakah ingin save? (Y/n) "))
if save.lower() == "y":
    save2 = str(input("Save dalam bentuk image? (Y/n) "))
    if save2.lower() == "y":
        filename = input("Masukkan lokasi dan nama file gambar (contoh: solusi.png): ")
        save_solution_image(board, queens, n, filename)
    else:
        filename = input("Masukkan lokasi dan nama file .txt (contoh: solusi.txt): ")
        try:
            with open(filename, 'w') as f:
                for row in FinalBoard:
                    f.write("".join(row) + "\n")
                print(f"Solusi berhasil disimpan di {filename}")
        except Exception as e:
            print(f"Error saat menyimpan file: {e}")

