// ==============================================================
// COPYRIGHT(c)2015, Galaxy Wind Co,Ltd
// All rights reserved.
//
// IP LIB INDEX  	: 
// IP Name       	:   
// 
// File name     	:   .v
// Module name   	:   
// 
// Author	        :   yangjianzhi
// Email     	    :   
// Data          	:   2018-09-03 10:29
// Last Modified    :   
// 
// Abstract			:
// 
// ==============================================================

module DICE_EOH_TOP(/*AUTOARG*/
   // Outputs
   dice_port9_data, dice_port9_ctrl, dice_port8_data, dice_port8_ctrl,
   dice_port7_data, dice_port7_ctrl, dice_port6_data, dice_port6_ctrl,
   dice_port5_data, dice_port5_ctrl, dice_port4_data, dice_port4_ctrl,
   dice_port3_data, dice_port3_ctrl, dice_port2_data, dice_port2_ctrl,
   dice_port1_data, dice_port1_ctrl, dice_port15_data,
   dice_port15_ctrl, dice_port14_data, dice_port14_ctrl,
   dice_port13_data, dice_port13_ctrl, dice_port12_data,
   dice_port12_ctrl, dice_port11_data, dice_port11_ctrl,
   dice_port10_data, dice_port10_ctrl, dice_port0_data,
   dice_port0_ctrl, dice0_ciu_int0, dice0_ciu_int1, EOH_INT1_out,
   dice_eoh_reg_chain_addr_out, dice_eoh_reg_chain_code_out,
   dice_eoh_reg_chain_data_out, dice_eoh_reg_chain_valid_out,
   eth_hptx_credit_release, eth_xb_data, eth_xb_release, eth_xb_vld,
   hirar0_slic_data, hirar0_slic_eop_valid, hirar0_slic_head,
   hirar0_slic_mop_valid, hirar0_slic_sop_valid, hirar0_slic_tail,
   dice0_cb_bypass_ciu_free, dice0_cb_egpipe_free,
   dice0_cb_gb_mop_free, dice0_cb_gb_sop_free, dice0_i1588_sqid_info,
   dice0_i1588_valid, dice0_qos_comp_info, dice0_qos_comp_wen,
   dice1_cb_bypass_ciu_free, dice1_cb_egpipe_free,
   dice1_cb_gb_mop_free, dice1_cb_gb_sop_free, dice_ciu_data,
   dice_ciu_data_valid, dice_ciu_head, dice_ciu_tail, dice_egr0_pd,
   dice_egr0_post_qd, dice_egr0_r2cpu_free, dice_egr0_sop,
   dice_egr0_sop_free, dice_egr0_sop_valid, dice_egr0_vlan_release,
   dice_port0_fifo_wr, dice_port10_fifo_wr, dice_port11_fifo_wr,
   dice_port12_fifo_wr, dice_port13_fifo_wr, dice_port14_fifo_wr,
   dice_port15_fifo_wr, dice_port1_fifo_wr, dice_port2_fifo_wr,
   dice_port3_fifo_wr, dice_port4_fifo_wr, dice_port5_fifo_wr,
   dice_port6_fifo_wr, dice_port7_fifo_wr, dice_port8_fifo_wr,
   dice_port9_fifo_wr, led_clk, led_data, table_ini_done,
   // Inputs
   port9_dice_pfc_pause, port8_dice_pfc_pause, port7_dice_pfc_pause,
   port6_dice_pfc_pause, port5_dice_pfc_pause, port4_dice_pfc_pause,
   port3_dice_pfc_pause, port2_dice_pfc_pause, port1_dice_pfc_pause,
   port15_dice_pfc_pause, port14_dice_pfc_pause,
   port13_dice_pfc_pause, port12_dice_pfc_pause,
   port11_dice_pfc_pause, port10_dice_pfc_pause, port0_dice_pfc_pause,
   sys_clk, rst_n, dice_eoh_reg_chain_addr_in,
   dice_eoh_reg_chain_code_in, dice_eoh_reg_chain_data_in,
   dice_eoh_reg_chain_valid_in, xb_eth_data, xb_eth_release,
   xb_eth_vld, xb_eth_fifo_credit_release, slic_hirar0_free,
   cb_dice0_bypass_valid, cb_dice0_egpipe_valid, cb_dice0_pkt,
   cb_dice0_qd, cb_dice1_bypass_valid, cb_dice1_egpipe_valid,
   cb_dice1_pkt, cb_dice1_qd, ciu_dice_free, egr0_dice_post_qd,
   egr0_dice_sop, egr0_dice_sop_free, egr0_dice_sop_valid,
   port0_dice_1588_timestamp, port0_dice_1588_valid,
   port0_dice_fifo_free, port10_dice_1588_timestamp,
   port10_dice_1588_valid, port10_dice_fifo_free,
   port11_dice_1588_timestamp, port11_dice_1588_valid,
   port11_dice_fifo_free, port12_dice_1588_timestamp,
   port12_dice_1588_valid, port12_dice_fifo_free,
   port13_dice_1588_timestamp, port13_dice_1588_valid,
   port13_dice_fifo_free, port14_dice_1588_timestamp,
   port14_dice_1588_valid, port14_dice_fifo_free,
   port15_dice_1588_timestamp, port15_dice_1588_valid,
   port15_dice_fifo_free, port1_dice_1588_timestamp,
   port1_dice_1588_valid, port1_dice_fifo_free,
   port2_dice_1588_timestamp, port2_dice_1588_valid,
   port2_dice_fifo_free, port3_dice_1588_timestamp,
   port3_dice_1588_valid, port3_dice_fifo_free,
   port4_dice_1588_timestamp, port4_dice_1588_valid,
   port4_dice_fifo_free, port5_dice_1588_timestamp,
   port5_dice_1588_valid, port5_dice_fifo_free,
   port6_dice_1588_timestamp, port6_dice_1588_valid,
   port6_dice_fifo_free, port7_dice_1588_timestamp,
   port7_dice_1588_valid, port7_dice_fifo_free,
   port8_dice_1588_timestamp, port8_dice_1588_valid,
   port8_dice_fifo_free, port9_dice_1588_timestamp,
   port9_dice_1588_valid, port9_dice_fifo_free, qos_dice0_comp_free,
   cb_seed, ecid, mac_seed, pcie_linkstate, port_linkup, portrx_valid,
   porttx_valid
   );
//==============================================================
//Function  : port
//Arguments : 
//==============================================================
//sys&clk/*{{{*/
input			sys_clk;		// To U_DICE0_TOP of DICE0_TOP.v, ...
input			rst_n;			// To U_DICE0_TOP of DICE0_TOP.v, ...
/*}}}*/
//int/*{{{*/
output			dice0_ciu_int0;		// From U_DICE0_TOP of DICE0_TOP.v
output			dice0_ciu_int1;		// From U_DICE0_TOP of DICE0_TOP.v
output			EOH_INT1_out;		// From U_EOH_TOP of EOH_TOP.v
/*}}}*/
//csr/*{{{*/
input [19:0]	dice_eoh_reg_chain_addr_in;// To U_DICE0_TOP of DICE0_TOP.v
input [3:0]		dice_eoh_reg_chain_code_in;// To U_DICE0_TOP of DICE0_TOP.v
input [63:0]	dice_eoh_reg_chain_data_in;// To U_DICE0_TOP of DICE0_TOP.v
input			dice_eoh_reg_chain_valid_in;// To U_DICE0_TOP of DICE0_TOP.v
output [19:0]	dice_eoh_reg_chain_addr_out;// From U_EOH_TOP of EOH_TOP.v
output [3:0]	dice_eoh_reg_chain_code_out;// From U_EOH_TOP of EOH_TOP.v
output [63:0]	dice_eoh_reg_chain_data_out;// From U_EOH_TOP of EOH_TOP.v
output			dice_eoh_reg_chain_valid_out;// From U_EOH_TOP of EOH_TOP.v
/*}}}*/
//xb&eth/*{{{*/
input [`XB_EOH_DATA_WIDTH-1:0] xb_eth_data;	// To U_EOH_TOP of EOH_TOP.v
input [7:0]		xb_eth_release;		// To U_EOH_TOP of EOH_TOP.v
input			xb_eth_vld;		// To U_EOH_TOP of EOH_TOP.v
output			eth_hptx_credit_release;// From U_EOH_TOP of EOH_TOP.v
output [`EOH_XB_DATA_WIDTH-1:0] eth_xb_data;	// From U_EOH_TOP of EOH_TOP.v
output [7:0]	eth_xb_release;		// From U_EOH_TOP of EOH_TOP.v
output			eth_xb_vld;		// From U_EOH_TOP of EOH_TOP.v
input			xb_eth_fifo_credit_release;// To U_EOH_TOP of EOH_TOP.v
/*}}}*/
//eoh to slicing/*{{{*/
output [`GATEWAY_SLICE_DATA_WIDTH-1:0] hirar0_slic_data;// From U_EOH_TOP of EOH_TOP.v
output			hirar0_slic_eop_valid;	// From U_EOH_TOP of EOH_TOP.v
output			hirar0_slic_head;	// From U_EOH_TOP of EOH_TOP.v
output			hirar0_slic_mop_valid;	// From U_EOH_TOP of EOH_TOP.v
output			hirar0_slic_sop_valid;	// From U_EOH_TOP of EOH_TOP.v
output			hirar0_slic_tail;	// From U_EOH_TOP of EOH_TOP.v
input			slic_hirar0_free;	// To U_EOH_TOP of EOH_TOP.v
/*}}}*/
//dicing/*{{{*/
input			cb_dice0_bypass_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			cb_dice0_egpipe_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_MOP_WID-1:0] cb_dice0_pkt;		// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_POST_QD_WID-1:0] cb_dice0_qd;	// To U_DICE0_TOP of DICE0_TOP.v
input			cb_dice1_bypass_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			cb_dice1_egpipe_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_MOP_WID-1:0] cb_dice1_pkt;		// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_POST_QD_WID-1:0] cb_dice1_qd;	// To U_DICE0_TOP of DICE0_TOP.v
input			ciu_dice_free;		// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_POST_QD_WID-1:0] egr0_dice_post_qd;// To U_DICE0_TOP of DICE0_TOP.v
input [`DICE_ETH_OUT_WID-1:0] egr0_dice_sop;	// To U_DICE0_TOP of DICE0_TOP.v
input			egr0_dice_sop_free;	// To U_DICE0_TOP of DICE0_TOP.v
input			egr0_dice_sop_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port0_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port0_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port0_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port10_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port10_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port10_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port11_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port11_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port11_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port12_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port12_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port12_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port13_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port13_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port13_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port14_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port14_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port14_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port15_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port15_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port15_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port1_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port1_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port1_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port2_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port2_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port2_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port3_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port3_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port3_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port4_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port4_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port4_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port5_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port5_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port5_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port6_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port6_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port6_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port7_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port7_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port7_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port8_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port8_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port8_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input [31:0]		port9_dice_1588_timestamp;// To U_DICE0_TOP of DICE0_TOP.v
input			port9_dice_1588_valid;	// To U_DICE0_TOP of DICE0_TOP.v
input			port9_dice_fifo_free;	// To U_DICE0_TOP of DICE0_TOP.v
input			qos_dice0_comp_free;	// To U_DICE0_TOP of DICE0_TOP.v
output			dice0_cb_bypass_ciu_free;// From U_DICE0_TOP of DICE0_TOP.v
output			dice0_cb_egpipe_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [9:0]		dice0_cb_gb_mop_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [9:0]		dice0_cb_gb_sop_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [54:0]		dice0_i1588_sqid_info;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice0_i1588_valid;	// From U_DICE0_TOP of DICE0_TOP.v
output [44:0]		dice0_qos_comp_info;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice0_qos_comp_wen;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice1_cb_bypass_ciu_free;// From U_DICE0_TOP of DICE0_TOP.v
output			dice1_cb_egpipe_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [9:0]		dice1_cb_gb_mop_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [9:0]		dice1_cb_gb_sop_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [512:0]		dice_ciu_data;		// From U_DICE0_TOP of DICE0_TOP.v
output			dice_ciu_data_valid;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_ciu_head;		// From U_DICE0_TOP of DICE0_TOP.v
output			dice_ciu_tail;		// From U_DICE0_TOP of DICE0_TOP.v
output [`DICE_EGR_PD_WID-1:0] dice_egr0_pd;	// From U_DICE0_TOP of DICE0_TOP.v
output [`DICE_POST_QD_WID-1:0] dice_egr0_post_qd;// From U_DICE0_TOP of DICE0_TOP.v
output			dice_egr0_r2cpu_free;	// From U_DICE0_TOP of DICE0_TOP.v
output [`DICE_SOP_WID-1:0] dice_egr0_sop;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_egr0_sop_free;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_egr0_sop_valid;	// From U_DICE0_TOP of DICE0_TOP.v
output [77:0]		dice_egr0_vlan_release;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port0_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port10_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port11_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port12_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port13_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port14_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port15_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port1_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port2_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port3_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port4_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port5_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port6_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port7_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port8_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
output			dice_port9_fifo_wr;	// From U_DICE0_TOP of DICE0_TOP.v
/*}}}*/
//led/*{{{*/
input [63:0]		cb_seed;		// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [255:0]		ecid;			// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [7:0]		mac_seed;		// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [(`LED_RANDNUM_PCIE_PORT)-1:0] pcie_linkstate;// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [(`LED_RANDNUM_MAC_PORT)-1:0] port_linkup;// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [(`LED_RANDNUM_MAC_PORT)-1:0] portrx_valid;// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
input [(`LED_RANDNUM_MAC_PORT)-1:0] porttx_valid;// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
output			led_clk;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
output			led_data;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
output			table_ini_done;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP.v
/*}}}*/
//==============================================================
//Function  : wire
//Arguments : auto 
//==============================================================
/*AUTOINPUT*/
// Beginning of automatic inputs (from unused autoinst inputs)
input [7:0]		port0_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port10_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port11_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port12_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port13_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port14_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port15_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port1_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port2_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port3_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port4_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port5_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port6_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port7_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port8_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
input [7:0]		port9_dice_pfc_pause;	// To U_DICE0_TOP of DICE0_TOP.v
// End of automatics
/*AUTOOUTPUT*/
// Beginning of automatic outputs (from unused autoinst outputs)
output [59:0]		dice_port0_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port0_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port10_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port10_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port11_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port11_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port12_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port12_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port13_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port13_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port14_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port14_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port15_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port15_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port1_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port1_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port2_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port2_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port3_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port3_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port4_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port4_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port5_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port5_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port6_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port6_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port7_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port7_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port8_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port8_data;	// From U_DICE0_TOP of DICE0_TOP.v
output [59:0]		dice_port9_ctrl;	// From U_DICE0_TOP of DICE0_TOP.v
output [575:0]		dice_port9_data;	// From U_DICE0_TOP of DICE0_TOP.v
// End of automatics
//autowire/*{{{*/
/*AUTOWIRE*/
// Beginning of automatic wires (for undeclared instantiated-module outputs)
wire [255:0]		dice_hirar0_data;	// From U_DICE0_TOP of DICE0_TOP.v
wire			dice_hirar0_data_valid;	// From U_DICE0_TOP of DICE0_TOP.v
wire			dice_hirar0_head;	// From U_DICE0_TOP of DICE0_TOP.v
wire			dice_hirar0_tail;	// From U_DICE0_TOP of DICE0_TOP.v
wire			hirar0_dice_free;	// From U_EOH_TOP of EOH_TOP.v
wire [19:0]		inner_reg_0_chain_addr;	// From U_DICE0_TOP of DICE0_TOP.v
wire [3:0]		inner_reg_0_chain_code;	// From U_DICE0_TOP of DICE0_TOP.v
wire [63:0]		inner_reg_0_chain_data;	// From U_DICE0_TOP of DICE0_TOP.v
wire			inner_reg_0_chain_valid;// From U_DICE0_TOP of DICE0_TOP.v
wire [19:0]		inner_reg_1_chain_addr;	// From U_EOH_TOP of EOH_TOP.v
wire [3:0]		inner_reg_1_chain_code;	// From U_EOH_TOP of EOH_TOP.v
wire [63:0]		inner_reg_1_chain_data;	// From U_EOH_TOP of EOH_TOP.v
wire			inner_reg_1_chain_valid;// From U_EOH_TOP of EOH_TOP.v
// End of automatics
/*}}}*/
//==============================================================
//Function  : module inst
//Arguments : dice
//==============================================================
//dice/*{{{*/
/*DICE0_TOP AUTO_TEMPLATE(
	.reg_chain_addr_in	    (dice_eoh_reg_chain_addr_in[]),
	.reg_chain_code_in	    (dice_eoh_reg_chain_code_in[]),
	.reg_chain_data_in	    (dice_eoh_reg_chain_data_in[]),
	.reg_chain_valid_in	    (dice_eoh_reg_chain_valid_in),

	.reg_chain_addr_out	    (inner_reg_0_chain_addr[]),
	.reg_chain_code_out	    (inner_reg_0_chain_code[]),
	.reg_chain_data_out	    (inner_reg_0_chain_data[]),
	.reg_chain_valid_out	(inner_reg_0_chain_valid),
);*/

DICE0_TOP
    U_DICE0_TOP(/*AUTOINST*/
		// Outputs
		.reg_chain_valid_out	(inner_reg_0_chain_valid), // Templated
		.reg_chain_code_out	(inner_reg_0_chain_code[3:0]), // Templated
		.reg_chain_addr_out	(inner_reg_0_chain_addr[19:0]), // Templated
		.reg_chain_data_out	(inner_reg_0_chain_data[63:0]), // Templated
		.dice0_ciu_int0		(dice0_ciu_int0),
		.dice0_ciu_int1		(dice0_ciu_int1),
		.dice0_cb_egpipe_free	(dice0_cb_egpipe_free),
		.dice0_cb_bypass_ciu_free(dice0_cb_bypass_ciu_free),
		.dice0_cb_gb_sop_free	(dice0_cb_gb_sop_free[9:0]),
		.dice0_cb_gb_mop_free	(dice0_cb_gb_mop_free[9:0]),
		.dice1_cb_egpipe_free	(dice1_cb_egpipe_free),
		.dice1_cb_bypass_ciu_free(dice1_cb_bypass_ciu_free),
		.dice1_cb_gb_sop_free	(dice1_cb_gb_sop_free[9:0]),
		.dice1_cb_gb_mop_free	(dice1_cb_gb_mop_free[9:0]),
		.dice0_qos_comp_wen	(dice0_qos_comp_wen),
		.dice0_qos_comp_info	(dice0_qos_comp_info[44:0]),
		.dice0_i1588_valid	(dice0_i1588_valid),
		.dice0_i1588_sqid_info	(dice0_i1588_sqid_info[54:0]),
		.dice_egr0_sop_valid	(dice_egr0_sop_valid),
		.dice_egr0_pd		(dice_egr0_pd[`DICE_EGR_PD_WID-1:0]),
		.dice_egr0_sop		(dice_egr0_sop[`DICE_SOP_WID-1:0]),
		.dice_egr0_post_qd	(dice_egr0_post_qd[`DICE_POST_QD_WID-1:0]),
		.dice_egr0_sop_free	(dice_egr0_sop_free),
		.dice_egr0_r2cpu_free	(dice_egr0_r2cpu_free),
		.dice_egr0_vlan_release	(dice_egr0_vlan_release[77:0]),
		.dice_hirar0_data_valid	(dice_hirar0_data_valid),
		.dice_hirar0_data	(dice_hirar0_data[255:0]),
		.dice_hirar0_head	(dice_hirar0_head),
		.dice_hirar0_tail	(dice_hirar0_tail),
		.dice_ciu_data_valid	(dice_ciu_data_valid),
		.dice_ciu_data		(dice_ciu_data[512:0]),
		.dice_ciu_head		(dice_ciu_head),
		.dice_ciu_tail		(dice_ciu_tail),
		.dice_port0_data	(dice_port0_data[575:0]),
		.dice_port1_data	(dice_port1_data[575:0]),
		.dice_port2_data	(dice_port2_data[575:0]),
		.dice_port3_data	(dice_port3_data[575:0]),
		.dice_port4_data	(dice_port4_data[575:0]),
		.dice_port5_data	(dice_port5_data[575:0]),
		.dice_port6_data	(dice_port6_data[575:0]),
		.dice_port7_data	(dice_port7_data[575:0]),
		.dice_port8_data	(dice_port8_data[575:0]),
		.dice_port9_data	(dice_port9_data[575:0]),
		.dice_port10_data	(dice_port10_data[575:0]),
		.dice_port11_data	(dice_port11_data[575:0]),
		.dice_port12_data	(dice_port12_data[575:0]),
		.dice_port13_data	(dice_port13_data[575:0]),
		.dice_port14_data	(dice_port14_data[575:0]),
		.dice_port15_data	(dice_port15_data[575:0]),
		.dice_port0_ctrl	(dice_port0_ctrl[59:0]),
		.dice_port1_ctrl	(dice_port1_ctrl[59:0]),
		.dice_port2_ctrl	(dice_port2_ctrl[59:0]),
		.dice_port3_ctrl	(dice_port3_ctrl[59:0]),
		.dice_port4_ctrl	(dice_port4_ctrl[59:0]),
		.dice_port5_ctrl	(dice_port5_ctrl[59:0]),
		.dice_port6_ctrl	(dice_port6_ctrl[59:0]),
		.dice_port7_ctrl	(dice_port7_ctrl[59:0]),
		.dice_port8_ctrl	(dice_port8_ctrl[59:0]),
		.dice_port9_ctrl	(dice_port9_ctrl[59:0]),
		.dice_port10_ctrl	(dice_port10_ctrl[59:0]),
		.dice_port11_ctrl	(dice_port11_ctrl[59:0]),
		.dice_port12_ctrl	(dice_port12_ctrl[59:0]),
		.dice_port13_ctrl	(dice_port13_ctrl[59:0]),
		.dice_port14_ctrl	(dice_port14_ctrl[59:0]),
		.dice_port15_ctrl	(dice_port15_ctrl[59:0]),
		.dice_port0_fifo_wr	(dice_port0_fifo_wr),
		.dice_port1_fifo_wr	(dice_port1_fifo_wr),
		.dice_port2_fifo_wr	(dice_port2_fifo_wr),
		.dice_port3_fifo_wr	(dice_port3_fifo_wr),
		.dice_port4_fifo_wr	(dice_port4_fifo_wr),
		.dice_port5_fifo_wr	(dice_port5_fifo_wr),
		.dice_port6_fifo_wr	(dice_port6_fifo_wr),
		.dice_port7_fifo_wr	(dice_port7_fifo_wr),
		.dice_port8_fifo_wr	(dice_port8_fifo_wr),
		.dice_port9_fifo_wr	(dice_port9_fifo_wr),
		.dice_port10_fifo_wr	(dice_port10_fifo_wr),
		.dice_port11_fifo_wr	(dice_port11_fifo_wr),
		.dice_port12_fifo_wr	(dice_port12_fifo_wr),
		.dice_port13_fifo_wr	(dice_port13_fifo_wr),
		.dice_port14_fifo_wr	(dice_port14_fifo_wr),
		.dice_port15_fifo_wr	(dice_port15_fifo_wr),
		// Inputs
		.sys_clk		(sys_clk),
		.rst_n			(rst_n),
		.reg_chain_valid_in	(dice_eoh_reg_chain_valid_in), // Templated
		.reg_chain_code_in	(dice_eoh_reg_chain_code_in[3:0]), // Templated
		.reg_chain_addr_in	(dice_eoh_reg_chain_addr_in[19:0]), // Templated
		.reg_chain_data_in	(dice_eoh_reg_chain_data_in[63:0]), // Templated
		.cb_dice0_bypass_valid	(cb_dice0_bypass_valid),
		.cb_dice0_egpipe_valid	(cb_dice0_egpipe_valid),
		.cb_dice0_pkt		(cb_dice0_pkt[`DICE_MOP_WID-1:0]),
		.cb_dice0_qd		(cb_dice0_qd[`DICE_POST_QD_WID-1:0]),
		.cb_dice1_bypass_valid	(cb_dice1_bypass_valid),
		.cb_dice1_egpipe_valid	(cb_dice1_egpipe_valid),
		.cb_dice1_pkt		(cb_dice1_pkt[`DICE_MOP_WID-1:0]),
		.cb_dice1_qd		(cb_dice1_qd[`DICE_POST_QD_WID-1:0]),
		.qos_dice0_comp_free	(qos_dice0_comp_free),
		.egr0_dice_sop_free	(egr0_dice_sop_free),
		.egr0_dice_sop_valid	(egr0_dice_sop_valid),
		.egr0_dice_post_qd	(egr0_dice_post_qd[`DICE_POST_QD_WID-1:0]),
		.egr0_dice_sop		(egr0_dice_sop[`DICE_ETH_OUT_WID-1:0]),
		.hirar0_dice_free	(hirar0_dice_free),
		.ciu_dice_free		(ciu_dice_free),
		.port0_dice_pfc_pause	(port0_dice_pfc_pause[7:0]),
		.port1_dice_pfc_pause	(port1_dice_pfc_pause[7:0]),
		.port2_dice_pfc_pause	(port2_dice_pfc_pause[7:0]),
		.port3_dice_pfc_pause	(port3_dice_pfc_pause[7:0]),
		.port4_dice_pfc_pause	(port4_dice_pfc_pause[7:0]),
		.port5_dice_pfc_pause	(port5_dice_pfc_pause[7:0]),
		.port6_dice_pfc_pause	(port6_dice_pfc_pause[7:0]),
		.port7_dice_pfc_pause	(port7_dice_pfc_pause[7:0]),
		.port8_dice_pfc_pause	(port8_dice_pfc_pause[7:0]),
		.port9_dice_pfc_pause	(port9_dice_pfc_pause[7:0]),
		.port10_dice_pfc_pause	(port10_dice_pfc_pause[7:0]),
		.port11_dice_pfc_pause	(port11_dice_pfc_pause[7:0]),
		.port12_dice_pfc_pause	(port12_dice_pfc_pause[7:0]),
		.port13_dice_pfc_pause	(port13_dice_pfc_pause[7:0]),
		.port14_dice_pfc_pause	(port14_dice_pfc_pause[7:0]),
		.port15_dice_pfc_pause	(port15_dice_pfc_pause[7:0]),
		.port0_dice_fifo_free	(port0_dice_fifo_free),
		.port1_dice_fifo_free	(port1_dice_fifo_free),
		.port2_dice_fifo_free	(port2_dice_fifo_free),
		.port3_dice_fifo_free	(port3_dice_fifo_free),
		.port4_dice_fifo_free	(port4_dice_fifo_free),
		.port5_dice_fifo_free	(port5_dice_fifo_free),
		.port6_dice_fifo_free	(port6_dice_fifo_free),
		.port7_dice_fifo_free	(port7_dice_fifo_free),
		.port8_dice_fifo_free	(port8_dice_fifo_free),
		.port9_dice_fifo_free	(port9_dice_fifo_free),
		.port10_dice_fifo_free	(port10_dice_fifo_free),
		.port11_dice_fifo_free	(port11_dice_fifo_free),
		.port12_dice_fifo_free	(port12_dice_fifo_free),
		.port13_dice_fifo_free	(port13_dice_fifo_free),
		.port14_dice_fifo_free	(port14_dice_fifo_free),
		.port15_dice_fifo_free	(port15_dice_fifo_free),
		.port0_dice_1588_valid	(port0_dice_1588_valid),
		.port1_dice_1588_valid	(port1_dice_1588_valid),
		.port2_dice_1588_valid	(port2_dice_1588_valid),
		.port3_dice_1588_valid	(port3_dice_1588_valid),
		.port4_dice_1588_valid	(port4_dice_1588_valid),
		.port5_dice_1588_valid	(port5_dice_1588_valid),
		.port6_dice_1588_valid	(port6_dice_1588_valid),
		.port7_dice_1588_valid	(port7_dice_1588_valid),
		.port8_dice_1588_valid	(port8_dice_1588_valid),
		.port9_dice_1588_valid	(port9_dice_1588_valid),
		.port10_dice_1588_valid	(port10_dice_1588_valid),
		.port11_dice_1588_valid	(port11_dice_1588_valid),
		.port12_dice_1588_valid	(port12_dice_1588_valid),
		.port13_dice_1588_valid	(port13_dice_1588_valid),
		.port14_dice_1588_valid	(port14_dice_1588_valid),
		.port15_dice_1588_valid	(port15_dice_1588_valid),
		.port0_dice_1588_timestamp(port0_dice_1588_timestamp[31:0]),
		.port1_dice_1588_timestamp(port1_dice_1588_timestamp[31:0]),
		.port2_dice_1588_timestamp(port2_dice_1588_timestamp[31:0]),
		.port3_dice_1588_timestamp(port3_dice_1588_timestamp[31:0]),
		.port4_dice_1588_timestamp(port4_dice_1588_timestamp[31:0]),
		.port5_dice_1588_timestamp(port5_dice_1588_timestamp[31:0]),
		.port6_dice_1588_timestamp(port6_dice_1588_timestamp[31:0]),
		.port7_dice_1588_timestamp(port7_dice_1588_timestamp[31:0]),
		.port8_dice_1588_timestamp(port8_dice_1588_timestamp[31:0]),
		.port9_dice_1588_timestamp(port9_dice_1588_timestamp[31:0]),
		.port10_dice_1588_timestamp(port10_dice_1588_timestamp[31:0]),
		.port11_dice_1588_timestamp(port11_dice_1588_timestamp[31:0]),
		.port12_dice_1588_timestamp(port12_dice_1588_timestamp[31:0]),
		.port13_dice_1588_timestamp(port13_dice_1588_timestamp[31:0]),
		.port14_dice_1588_timestamp(port14_dice_1588_timestamp[31:0]),
		.port15_dice_1588_timestamp(port15_dice_1588_timestamp[31:0]));
/*}}}*/
//==============================================================
//Function  : module inst
//Arguments : eoh
//==============================================================
//eoh/*{{{*/
/*EOH_TOP AUTO_TEMPLATE(
	.reg_chain_addr_in	    (inner_reg_0_chain_addr[]),
	.reg_chain_code_in	    (inner_reg_0_chain_code[]),
	.reg_chain_data_in	    (inner_reg_0_chain_data[]),
	.reg_chain_valid_in	    (inner_reg_0_chain_valid),
	.reg_chain_addr_out	    (inner_reg_1_chain_addr[]),
	.reg_chain_code_out	    (inner_reg_1_chain_code[]),
	.reg_chain_data_out	    (inner_reg_1_chain_data[]),
	.reg_chain_valid_out	(inner_reg_1_chain_valid),

    .hirar_dice_free        (hirar0_dice_free      ),
    .dice_hirar_data_valid  (dice_hirar0_data_valid),
    .dice_hirar_data        (dice_hirar0_data[]    ),
    .dice_hirar_head        (dice_hirar0_head      ),
    .dice_hirar_tail        (dice_hirar0_tail      ),

    .hirar_slic_data        (hirar0_slic_data[]    ),
    .hirar_slic_eop_valid   (hirar0_slic_eop_valid ),
    .hirar_slic_head        (hirar0_slic_head      ),
    .hirar_slic_mop_valid   (hirar0_slic_mop_valid ),
    .hirar_slic_sop_valid   (hirar0_slic_sop_valid ),
    .hirar_slic_tail        (hirar0_slic_tail      ),
    .slic_hirar_free        (slic_hirar0_free      ),
);*/
EOH_TOP
    U_EOH_TOP(/*AUTOINST*/
	      // Outputs
	      .eth_hptx_credit_release	(eth_hptx_credit_release),
	      .eth_xb_data		(eth_xb_data[`EOH_XB_DATA_WIDTH-1:0]),
	      .reg_chain_addr_out	(inner_reg_1_chain_addr[19:0]), // Templated
	      .reg_chain_code_out	(inner_reg_1_chain_code[3:0]), // Templated
	      .reg_chain_data_out	(inner_reg_1_chain_data[63:0]), // Templated
	      .reg_chain_valid_out	(inner_reg_1_chain_valid), // Templated
	      .EOH_INT1_out		(EOH_INT1_out),
	      .eth_xb_release		(eth_xb_release[7:0]),
	      .eth_xb_vld		(eth_xb_vld),
	      .hirar_dice_free		(hirar0_dice_free      ), // Templated
	      .hirar_slic_data		(hirar0_slic_data[`GATEWAY_SLICE_DATA_WIDTH-1:0]    ), // Templated
	      .hirar_slic_eop_valid	(hirar0_slic_eop_valid ), // Templated
	      .hirar_slic_head		(hirar0_slic_head      ), // Templated
	      .hirar_slic_mop_valid	(hirar0_slic_mop_valid ), // Templated
	      .hirar_slic_sop_valid	(hirar0_slic_sop_valid ), // Templated
	      .hirar_slic_tail		(hirar0_slic_tail      ), // Templated
	      // Inputs
	      .xb_eth_data		(xb_eth_data[`XB_EOH_DATA_WIDTH-1:0]),
	      .xb_eth_fifo_credit_release(xb_eth_fifo_credit_release),
	      .sys_clk			(sys_clk),
	      .rst_n			(rst_n),
	      .reg_chain_addr_in	(inner_reg_0_chain_addr[19:0]), // Templated
	      .reg_chain_code_in	(inner_reg_0_chain_code[3:0]), // Templated
	      .reg_chain_data_in	(inner_reg_0_chain_data[63:0]), // Templated
	      .reg_chain_valid_in	(inner_reg_0_chain_valid), // Templated
	      .xb_eth_release		(xb_eth_release[7:0]),
	      .xb_eth_vld		(xb_eth_vld),
	      .dice_hirar_data		(dice_hirar0_data[`GATEWAY_DICE_DATA_WIDTH-1:0]    ), // Templated
	      .dice_hirar_data_valid	(dice_hirar0_data_valid), // Templated
	      .dice_hirar_head		(dice_hirar0_head      ), // Templated
	      .dice_hirar_tail		(dice_hirar0_tail      ), // Templated
	      .slic_hirar_free		(slic_hirar0_free      )); // Templated
/*}}}*/
//==============================================================
//Function  : module inst
//Arguments : led
//==============================================================
//led/*{{{*/
/*LED_RANDNUM_TOP AUTO_TEMPLATE(
    .mac_smp_clk            (sys_clk                   ),
    .reg_chain_valid_in     (inner_reg_1_chain_valid   ),
    .reg_chain_code_in      (inner_reg_1_chain_code[]  ),
    .reg_chain_addr_in      (inner_reg_1_chain_addr[]  ),
    .reg_chain_data_in      (inner_reg_1_chain_data[]  ),
    .reg_chain_valid_out    (dice_eoh_reg_chain_valid_out),
    .reg_chain_code_out     (dice_eoh_reg_chain_code_out[]),
    .reg_chain_addr_out     (dice_eoh_reg_chain_addr_out[]),
    .reg_chain_data_out     (dice_eoh_reg_chain_data_out[]),

    .mac_mdio_sel0          (),
    .mac_mdio_sel1          (),
    .mac_mdio_sel           (),

    .phy_mdi                (1'b0),
    .phy_mdc                (),
    .phy_mdo_en             (),
    .phy_mdo                (),

    //need to modify
    .port_likup             (port_linkup[]),
    //hirar not used
    .p0_llp_light           (2'd0),
    .p1_llp_light           (2'd0),
    .hirar0_mode            (),
    .hirar1_mode            (),

);*/
LED_RANDNUM_TOP
    U_LED_RANDNUM_TOP(/*AUTOINST*/
		      // Outputs
		      .reg_chain_valid_out(dice_eoh_reg_chain_valid_out), // Templated
		      .reg_chain_code_out(dice_eoh_reg_chain_code_out[3:0]), // Templated
		      .reg_chain_addr_out(dice_eoh_reg_chain_addr_out[19:0]), // Templated
		      .reg_chain_data_out(dice_eoh_reg_chain_data_out[63:0]), // Templated
		      .mac_mdio_sel0	(),			 // Templated
		      .mac_mdio_sel1	(),			 // Templated
		      .mac_mdio_sel	(),			 // Templated
		      .hirar0_mode	(),			 // Templated
		      .hirar1_mode	(),			 // Templated
		      .table_ini_done	(table_ini_done),
		      .led_clk		(led_clk),
		      .led_data		(led_data),
		      .phy_mdc		(),			 // Templated
		      .phy_mdo_en	(),			 // Templated
		      .phy_mdo		(),			 // Templated
		      // Inputs
		      .sys_clk		(sys_clk),
		      .mac_smp_clk	(sys_clk                   ), // Templated
		      .rst_n		(rst_n),
		      .reg_chain_valid_in(inner_reg_1_chain_valid   ), // Templated
		      .reg_chain_code_in(inner_reg_1_chain_code[3:0]  ), // Templated
		      .reg_chain_addr_in(inner_reg_1_chain_addr[19:0]  ), // Templated
		      .reg_chain_data_in(inner_reg_1_chain_data[63:0]  ), // Templated
		      .porttx_valid	(porttx_valid[(`LED_RANDNUM_MAC_PORT)-1:0]),
		      .portrx_valid	(portrx_valid[(`LED_RANDNUM_MAC_PORT)-1:0]),
		      .port_linkup	(port_linkup[(`LED_RANDNUM_MAC_PORT)-1:0]),
		      .mac_seed		(mac_seed[7:0]),
		      .pcie_linkstate	(pcie_linkstate[(`LED_RANDNUM_PCIE_PORT)-1:0]),
		      .p0_llp_light	(2'd0),			 // Templated
		      .p1_llp_light	(2'd0),			 // Templated
		      .ecid		(ecid[255:0]),
		      .cb_seed		(cb_seed[63:0]),
		      .phy_mdi		(1'b0));			 // Templated
/*}}}*/
endmodule
//Local Variables:
//verilog-library-directories:(".")
//verilog-library-files:("../eoh_gateway/source_code/eoh_top.v"
//"~/es8000_hw_code/es9600_hw_code/trunk/asic/design_code/top/source_code/led_randnum/source_code/led_randnum_top.v"
//                       "../dice/source_code/dice0_top.v")
//verilog-library-extensions:(".v" ".h")
//verilog-auto-inst-param-value:t
//End:


