# Makefile for Robotics course, python version
# $Id: Makefile,v 1.30 2016/06/05 13:46:07 arnoud Exp $
# Based on Java versie van Matthijs Spaan en Olaf Booij

.PHONY: software4students
software4students:
	mkdir -p software4students
	cp chessgame_STUDENTS.py software4students/chessgame.py
	cp board.chb software4students/
	cp joints_simulator.txt software4students/
	cp umi_chessboard.py software4students/
	cp umi_common.py software4students/
	cp umi_parameters_STUDENTS.py software4students/umi_parameters.py
	cp umi_simulation.py software4students/
	cp umi_student_functions.py software4students/
	cp -pr board_configurations software4students/
	
software4students.tgz: software4students
	tar cvfz software4students.tgz software4students/* 	

JAVAFILES =  BoardLocation.java ChessBoard.java ChessPiece.java\
 GripperPosition.java JointValues.java Point.java Vector3D.java\
 RobotJoints.java IKstandard.java PPstandard.java
CLASSFILES = $(subst java,class,${JAVAFILES})\
 ChessBoard\$$NoPieceAtPositionException.class RobotJoints\$$Joint.class
HINTSFILES = hints/DOCUMENTATION hints/GETTING_STARTED hints/HIGHPATH_POSITIONS
ENDGAMEFILES = pl/chess.pl pl/KRAProok.pl \
 pl/KRPL.pl pl/KRPLrook.pl pl/AL0.pl pl/readGnuChessrFile.pl
BINARYFILES = playchess endgamerook endgamepawn #endgamequeen endgamerookrook #??? testIK
DATAFILES = data/board.rtx data/pieces.rtx data/umi.rtx data/endgamerook.gch data/endgamequeen.gch data/endgamepawn.gch #data/endgamerookrook1.gch data/endgamerookrook2.gch data/endgamerookrook3.gch data/endgamerookrook4.gch 

MY_ROBOTICSHOME = /home/arnoud/onderwijs/ZSB/assistance
ROBOTICSHOME = /opt/stud/robotics
HIDDENROBOTICSHOME = /opt/stud/robotics/assistance
LOCALROBOTICSHOME = ..

USEROBOTICSHOME = $(LOCALROBOTICSHOME)

DOCHOME = ${ROBOTICSHOME}/doc
CLASSHOME = ${ROBOTICSHOME}/class
SOFTWAREHOME = ${ROBOTICSHOME}/software4students
#SOFTWAREHOME = ../zsb
BINARYHOME = ${ROBOTICSHOME}/bin
DATAHOME = ${ROBOTICSHOME}/data

CP = cp -vu

CC = gcc
CFLAGS = -O2 -g -Wall
INCLUDE = -I${USEROBOTICSHOME}/robotics/include
LIBS = ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libstub.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libumi.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libxmlparser.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libmatrix.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/librtxmove.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libchess.a -lm
LIBS = ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libstub.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libmatrix.a \
 ${USEROBOTICSHOME}/robotics/lib/$(MACHINE)/libchess.a -lm

all: baseClasses IK PP playchess 

IKstandard.java: IK.java
	sed "s/class IK/class IKstandard/g" IK.java > IKstandard.java

PPstandard.java: PP.java
	sed "s/class PP/class PPstandard/g" PP.java > PPstandard.java

IK:
	${JAVAC} IK.java

PP:
	${JAVAC} PP.java

baseClasses: ${JAVAFILES}
	${JAVAC} ${JAVAFILES}

clean:
	rm -f *~ *.class *.so *.o ${BINARYFILES}

doc:	.force
	# pfff
	mv Week2.java Week2.java.hidden
	mv Week6.java Week6.java.hidden
	javadoc -d ${DOCHOME} -version -author\
 -windowtitle "Robotics course documentation" ${JAVAFILES}
	mv Week2.java.hidden Week2.java
	mv Week6.java.hidden Week6.java
	cd ${DOCHOME}; \
	scp -r * obooij@remote:public_html/teaching/search_navigate/doc/

tar:
	cd ${ROBOTICSHOME}; \
	gtar cvfz robotica.tar.gz class/ doc/

playchess: playchess.o endgamerook endgamequeen endgamepawn endgamerookrook
	${CC} -o playchess playchess.o ${LIBS}

endgamerook: playchess.c
	${CC} ${CFLAGS} ${INCLUDE} -DENDGAME -DROOK -o endgamerook playchess.c ${LIBS}

endgamequeen: playchess.c
	${CC} ${CFLAGS} ${INCLUDE} -DENDGAME -DQUEEN -o endgamequeen playchess.c ${LIBS}

endgamepawn: playchess.c
	${CC} ${CFLAGS} ${INCLUDE} -DENDGAME -DPAWN -o endgamepawn playchess.c ${LIBS}

endgamerookrook: playchess.c
	${CC} ${CFLAGS} ${INCLUDE} -DENDGAME -DROOKROOK -o endgamerookrook playchess.c ${LIBS}

testIK: testIK.o
	${CC} -o testIK testIK.o ${LIBS}

install:
	@${CP} ${CLASSFILES} ${CLASSHOME}
	@${CP} Week1.java ${SOFTWAREHOME}/pp/BoardTrans.java
	@${CP} Week2.java ${SOFTWAREHOME}/pp/PP.java
	@${CP} DistanceMatrix.java ${SOFTWAREHOME}/pp/
	@${CP} Week6.java ${SOFTWAREHOME}/ik/IK.java
	@${CP} ${ENDGAMEFILES} ${SOFTWAREHOME}/pl/
	@${CP} pl/KRAPpawn.empty.pl ${SOFTWAREHOME}/pl/KRAPpawn.pl
	@${CP} pl/KRPLpawn.empty.pl ${SOFTWAREHOME}/pl/KRPLpawn.pl
	@${CP} ${BINARYFILES} ${BINARYHOME}/
	@${CP} ${HINTSFILES} ${ROBOTICSHOME}/hints/
	@${CP} README.CVS ${ROBOTICSHOME}/assistance/
	@${CP} ${DATAFILES} ${DATAHOME}/

.force:

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDE) -c $<
