import getopt
import sys
q={}
tags = ['noun', 'verb','inf',  'prep']


def printresults(pieTable, backpointer, finalseq, forward,words):
    print "FINAL VITERBI NETWORK"
    for i in range(1, len(pieTable)-1):
        for j in range(len(tags)):
            print ("P(" + words[i - 1] + "=" + tags[j] + ")=" + '%.10f') % (pieTable[i][j])
    print ''

    print "FINAL BACKPTR NETWORK"
    for i in range(2, len(backpointer)):
        for j in range(len(tags)):
            print ("Backptr(" + words[i - 1] + "=" + tags[j] + ")=" + backpointer[i][j])
    print ''

    print ("BEST TAG SEQUENCE HAS PROBABILITY="+ '%.10f')%max(pieTable[-1])
    for i in range(len(words)-1,-1,-1):
        print words[i]+" -> "+finalseq[i]
    print ''

    print "FORWARD ALGORITHM RESULTS"
    for i in range(1, len(forward)):
        for j in range(len(tags)):
            print ("P(" + words[i - 1] + "=" + tags[j] + ")=" + '%.10f') % (forward[i][j])
    
    print ''

def viterbi(sent):
    words=sent.split()
    backpointer=[['' for i in range(len(tags))] for j in range(len(words)+1)]
    finalseq=['' for i in range(len(words))]
    pieTable = [[0 for i in range(len(tags))] for j in range(len(words)+2)]
    forward= [[0 for i in range(len(tags))] for j in range(len(words)+1)]
    for i in range(len(tags)):
        pieTable[0][i]= q.get(tags[i]+"phi",0.0001)

    for i in range(1,len(words)+1):
        for j in range(len(tags)):
            for k in range(len(tags)):
                if i==1:
                    pieTable[i][j] = max(pieTable[i][j], pieTable[i - 1][j] * q.get(words[i - 1] + tags[j], 0.0001))
                    forward[i][j]=  (pieTable[i - 1][j] * q.get(words[i - 1] + tags[j], 0.0001))
                else:
                    value=pieTable[i-1][k]*q.get(tags[j]+tags[k],0.0001)*q.get(words[i-1]+tags[j],0.0001)

                    if value>pieTable[i][j]:
                        backpointer[i][j]=tags[k]

                    pieTable[i][j]=max(pieTable[i][j],value)
                    forward[i][j]= sum((forward[i][j],value))
        finalseq[i - 1] = tags[pieTable[i].index(max(pieTable[i]))]
    for i in range(len(tags)):
        pieTable[-1][i] = max(pieTable[-1][i],pieTable[-2][i] * q.get("fin" + tags[i] , 0.0001))

    printresults(pieTable,backpointer,finalseq,forward,words)


def processQ(probs):
    with open(probs) as probfile:
        output = probfile.read()
        output=output.splitlines()

    for i in output:
        i.lower
        values=i.split()
        q[(values[0])+(values[1])]=float(values[2])

def main():
    (options, args) = getopt.getopt(sys.argv[1:], '')
    processQ(args[0])
    with open(args[1]) as data:
        lines = data.read().splitlines()

    for line in lines:
        print "PROCESSING SENTENCE: " + line
        print ''
        line.lower
        viterbi(line)



if __name__ == "__main__":
    main()

