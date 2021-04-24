
inp = 'lichess_db_standard_rated_2017-04.pgn'
inp = 'games.pgn'
import bz2
import pandas as pd
lists = []
s_list = {}
with bz2.open(inp+'.bz2','rt') as z:
        for line in z:
            if(line[0]=='['):
                p1 = line.strip('[]').split()[0]
                p2 = line.split('"')[1]
                s_list.update({p1:p2})
            else:
                if(len(s_list)>1):
                    if ( s_list.get('Event') == 'Rated Blitz game'):
                        lists.append(s_list)
                    s_list={}

#
import time
# p = time.time()
# pd.concat(([pd.Series(i).to_frame().transpose() for i in lists]))
# time.time() - p


p = time.time()
df1 = pd.DataFrame.from_dict(lists)
time.time() - p
df1.to_csv('output.csv')










def preprocess_PGN(inp, maxlim, blunder_cutoff, min_elo, max_elo, min_time, max_time):
    print("Starting...")
    id_string = "time" + str(min_time) + "-" + str(max_time) + "_rating" + str(min_elo) + "-" + str(max_elo)
    if not maxlim:
        maxlim = float("Inf")
    start = int(time.time())
    linecount = 0
    validcount = 0
    curr_elo = -1
    normalization = {}
    finished = False
    out = "data/" + str(start) + " " + id_string + "_raw.txt"
    normout = "data/" + str(start) + " " + id_string + "_norm.txt"
    infoout = "data/" + str(start) + " " + id_string + "_info.txt"
    with open(inp, "r") as infile:
        with open(out, "w") as outfile:
            for line in infile:
                if linecount > maxlim:
                    break
                    # return normalization
                if line[:9] == "[WhiteElo":
                    curr_elo = int(line.split()[1][1:-2])
                if (curr_elo < max_elo) and (curr_elo >= min_elo) and (line[:3] == "1. "):
                    # reset for new game!
                    stripped = strip_game(line, min_time, max_time)
                    if stripped:
                        validcount += 1
                        blunder_times, normalization = extract_blunders(stripped, normalization)
                        for t in blunder_times:
                            outfile.write(str(t) + "\n")
                linecount += 1
    time_taken = time.time() - start
    print("Finished creating", out, " after ", linecount, " lines processed. (", validcount, " matching games found)")
    print(round(time_taken, 3), " seconds taken.")
    with open(normout, "w") as outfile:
        print(normalization, file=outfile)
    with open(infoout, "w") as outfile:
        print("Created", out, "\n", linecount, " lines processed. (", validcount, " matching games found)",
              file=outfile)
        print(str(time_taken) + " seconds taken.", file=outfile)
        print("\nParameters used:", file=outfile)
        print("\n Blunder cutoff: ", blunder_cutoff, "\nMin Elo: ", min_elo, "\nMax Elo: ", max_elo, "\nMin time:",
              min_time, "\nMax time:", max_time, file=outfile)
    return normalization, out
