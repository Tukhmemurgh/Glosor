import json
from textblob import TextBlob
import xlrd
import os
import random

class Glosor():
    def __init__(self, sheet):
        self.sheet = sheet
        self.data = {self.sheet.row_values(i)[0]:self.sheet.row_values(i)[1] for i in range(len(self.sheet.col_values(0)))}

    def Healthy(self):
        pass

def main():
    wb = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), 'excelfiles', 'ord.xlsx'))
    sheets = wb.sheet_names()
    print("Hej! Följande sheets finns i excel-arket:")
    print("--------------------------------------------------")
    for i, sheet in enumerate(sheets):
        print("|",i, "|\t", sheet)
        print("--------------------------------------------------")
    done = False
    while not done:
        s1 = input("Var god skriv in index på arket du vill öppna: ")
        if not s1.isdigit():
            print("Du måste svara med ett index.")
            continue
        elif s1.isdigit() and not isinstance(int(s1), int):
            print("Du måste svara med ett index som är ett tillräckligt litet positivt heltal.")
            continue
        elif s1.isdigit() and isinstance(int(s1), int) and int(s1) > len(sheets):
            print("Du måste svara med ett index som är ett tillräckligt litet positivt heltal.")
            continue
        done = True
    print("--------------------------------------------------")
    print("Vill du öva på den svenska eller japanska översättningen? Dvs, vill du få ett japanskt ord av programmet och översätta det till svenska eller vice versa?")
    done = False
    while not done:
        s2 = input("Svara med 1 för att få ord på japanska och 2 för att få ord på svenska: ")
        if s2 != '1' and s2 != '2':
            print("Du måste svara med 1 eller 2.")
            continue
        done = True
    print("--------------------------------------------------")
    print("Vill du öva skriftligt eller auditivt?")
    done = False
    while not done:
        s3 = input("Svara med 'skriftligt' för skriftligt och 'auditivt' för auditivt: ")
        if s3 != 'skriftligt' and s3 != 'auditivt':
            print("Du måste svara med 1 eller 2.")
            continue
        done = True
    sheet = wb.sheet_by_index(int(s1))
    glosor = Glosor(sheet)
    print("--------------------------------------------------")
    score = 0
    tries = 0
    closed = False
    while not closed:
        temp_glosor = glosor.data.copy()
        if s2 == '1':
            print("Du har valt att öva på",s1,s3,"där du får input på japanska och svarar på svenska.")
            finished = False
            while not finished:
                tries += 1
                ord_sv, ord_ja = random.choice(list(temp_glosor.items()))
                print("Ord på japanska: " + ord_ja)
                ans = input("Ord på svenska: ")
                if ans == ord_sv and len(temp_glosor) > 1:
                    del temp_glosor[ord_sv]
                    print("Rätt!")
                    score += 1
                elif ans == ord_sv and len(temp_glosor) == 1:
                    score+=1
                    finished = True
                    print("Bra jobbat! Nu har du gått igenom alla glosorna")
                else:
                    print("Fel, svaret är " + ord_sv + ".")
                print("--------------------------------------------------")
            print("Av", tries, "försök fick du", score, "stycken rätt.")

        elif s2 == '2':
            print("Du har valt att öva på",s1,s3,"där du får input på svenska och svarar på japanska.")
            finished = False
            while not finished:
                tries += 1
                ord_sv, ord_ja = random.choice(list(temp_glosor.items()))
                print("Ord på svenska: " + ord_sv)
                ans = input("Ord på japanska: ")
                if ans == ord_ja and len(temp_glosor) > 1:
                    del temp_glosor[ord_sv]
                    print("Rätt!")
                    score += 1
                elif ans == ord_ja and len(temp_glosor) == 1:
                    score+=1
                    finished = True
                    print("Bra jobbat! Nu har du gått igenom alla glosorna")
                else:
                    print("Fel, svaret är " + ord_ja + ".")
                print("--------------------------------------------------")
            print("Av", tries, "fick du", score, "stycken rätt.")
        print("Vill du köra samma upplägg igen eller stänga av?")
        s4 = input("Svara med 'igen' eller 'stäng': ")
        if s4 == 'igen':
            print('Vill du ändra ordningen på språken?')
            s5 = input("Svara med 'ja' eller 'nej': ")
            if s5 == 'ja' and s2 == '1':
                s2='2'
                continue
            elif s5 == 'ja' and s2 == '2':
                s2='1'
                continue
            elif s5 == 'nej':
                continue
        elif s4 == 'stäng':
            closed = True
        print("--------------------------------------------------")
    print("Hejdå!")

def input_japanska(glosor):
    pass

def input_svenska(glosor):
    pass

if __name__ == '__main__':
    main()
