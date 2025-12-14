module LeaderRed(
    input  wire selectLeaderRed,
    input  wire leaderSignalRed,
    input  wire repLeaderRed,
    output wire pRepLeaderRed,
    output wire pDeadRed,
    output wire recNodeRed,
    output wire leaderSignalRedOut
);
wire activateLeaderRed;
assign activateLeaderRed  = selectLeaderRed & leaderSignalRed;
assign pRepLeaderRed      = activateLeaderRed;
assign pDeadRed           = activateLeaderRed;
assign recNodeRed         = repLeaderRed;
assign leaderSignalRedOut = ~recNodeRed;
endmodule

module ColorRed(
    input  wire PleaderSignalRed,
    input  wire nRFP,
    output wire recNodeRFP,
    output wire colorRFP
);
assign recNodeRFP = PleaderSignalRed & ~nRFP;
assign colorRFP   = recNodeRFP;
endmodule

module BandRed(
    input  wire lacMRed,
    input  wire lacRed,
    output wire bandRed
);
assign bandRed = ~lacMRed & ~lacRed;
endmodule

module DeadRed(
    input  wire bandRed,
    output wire deadRed
);
assign deadRed = bandRed;
endmodule

module SelectLeaderRed(
    input  wire bandGreen,
    input  wire bandYellow,
    output wire selectLeaderRed
);
assign selectLeaderRed = bandGreen & bandYellow;
endmodule

module LeaderGreen(
    input  wire selectLeaderGreen,
    input  wire leaderSignalGreen,
    input  wire repLeaderGreen,
    output wire pRepLeaderGreen,
    output wire pDeadGreen,
    output wire recNodeGreen,
    output wire leaderSignalGreenOut
);
wire activateLeaderGreen;
assign activateLeaderGreen  = selectLeaderGreen & leaderSignalGreen;
assign pRepLeaderGreen      = activateLeaderGreen;
assign pDeadGreen           = activateLeaderGreen;
assign recNodeGreen         = repLeaderGreen;
assign leaderSignalGreenOut = ~recNodeGreen;
endmodule

module ColorGreen(
    input  wire PleaderSignalGreen,
    input  wire nGFP,
    output wire recNodeGFP,
    output wire colorGFP
);
assign recNodeGFP = PleaderSignalGreen & ~nGFP;
assign colorGFP   = recNodeGFP;
endmodule

module BandGreen(
    input  wire lacMGreen,
    input  wire lacGreen,
    output wire bandGreen
);
assign bandGreen = ~lacMGreen & ~lacGreen;
endmodule

module DeadGreen(
    input  wire bandGreen,
    output wire deadGreen
);
assign deadGreen = bandGreen;
endmodule

module SelectLeaderGreen(
    input  wire bandRed,
    input  wire bandYellow,
    output wire selectLeaderGreen
);
assign selectLeaderGreen = bandRed & bandYellow;
endmodule

module LeaderYellow(
    input  wire selectLeaderYellow,
    input  wire leaderSignalYellow,
    input  wire repLeaderYellow,
    output wire pRepLeaderYellow,
    output wire pDeadYellow,
    output wire recNodeYellow,
    output wire leaderSignalYellowOut
);
wire activateLeaderYellow;
assign activateLeaderYellow  = selectLeaderYellow & leaderSignalYellow;
assign pRepLeaderYellow      = activateLeaderYellow;
assign pDeadYellow           = activateLeaderYellow;
assign recNodeYellow         = repLeaderYellow;
assign leaderSignalYellowOut = ~recNodeYellow;
endmodule

module ColorYellow(
    input  wire PleaderSignalYellow,
    input  wire nYFP,
    output wire recNodeYFP,
    output wire colorYFP
);
assign recNodeYFP = PleaderSignalYellow & ~nYFP;
assign colorYFP   = recNodeYFP;
endmodule

module BandYellow(
    input  wire lacMYellow,
    input  wire lacYellow,
    output wire bandYellow
);
assign bandYellow = ~lacMYellow & ~lacYellow;
endmodule

module DeadYellow(
    input  wire bandYellow,
    output wire deadYellow
);
assign deadYellow = bandYellow;
endmodule

module SelectLeaderYellow(
    input  wire bandRed,
    input  wire bandGreen,
    output wire selectLeaderYellow
);
assign selectLeaderYellow = bandRed & bandGreen;
endmodule
