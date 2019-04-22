module MAC_LED_TOP(/*AUTOARG*/
   // Outputs
   table_ini_done, port9_slic_data_valid, port9_slic_data,
   port9_slic_ctl, port9_dice_fifo_free, port9_dice_1588_valid,
   port9_dice_1588_timestamp, port8_slic_data_valid, port8_slic_data,
   port8_slic_ctl, port8_dice_fifo_free, port8_dice_1588_valid,
   port8_dice_1588_timestamp, port7_slic_data_valid, port7_slic_data,
   port7_slic_ctl, port7_dice_fifo_free, port7_dice_1588_valid,
   port7_dice_1588_timestamp, port6_slic_data_valid, port6_slic_data,
   port6_slic_ctl, port6_dice_fifo_free, port6_dice_1588_valid,
   port6_dice_1588_timestamp, port5_slic_data_valid, port5_slic_data,
   port5_slic_ctl, port5_dice_fifo_free, port5_dice_1588_valid,
   port5_dice_1588_timestamp, port4_slic_data_valid, port4_slic_data,
   port4_slic_ctl, port4_dice_fifo_free, port4_dice_1588_valid,
   port4_dice_1588_timestamp, port3_slic_data_valid, port3_slic_data,
   port3_slic_ctl, port3_dice_fifo_free, port3_dice_1588_valid,
   port3_dice_1588_timestamp, port2_slic_data_valid, port2_slic_data,
   port2_slic_ctl, port2_dice_fifo_free, port2_dice_1588_valid,
   port2_dice_1588_timestamp, port1_slic_data_valid, port1_slic_data,
   port1_slic_ctl, port1_dice_fifo_free, port1_dice_1588_valid,
   port1_dice_1588_timestamp, port15_slic_data_valid,
   port15_slic_data, port15_slic_ctl, port15_dice_fifo_free,
   port15_dice_1588_valid, port15_dice_1588_timestamp,
   port14_slic_data_valid, port14_slic_data, port14_slic_ctl,
   port14_dice_fifo_free, port14_dice_1588_valid,
   port14_dice_1588_timestamp, port13_slic_data_valid,
   port13_slic_data, port13_slic_ctl, port13_dice_fifo_free,
   port13_dice_1588_valid, port13_dice_1588_timestamp,
   port12_slic_data_valid, port12_slic_data, port12_slic_ctl,
   port12_dice_fifo_free, port12_dice_1588_valid,
   port12_dice_1588_timestamp, port11_slic_data_valid,
   port11_slic_data, port11_slic_ctl, port11_dice_fifo_free,
   port11_dice_1588_valid, port11_dice_1588_timestamp,
   port10_slic_data_valid, port10_slic_data, port10_slic_ctl,
   port10_dice_fifo_free, port10_dice_1588_valid,
   port10_dice_1588_timestamp, port0_slic_data_valid, port0_slic_data,
   port0_slic_ctl, port0_dice_fifo_free, port0_dice_1588_valid,
   port0_dice_1588_timestamp, mport1_mii0_pcs_txd,
   mport1_mii0_pcs_txc, mport1_mac_int, mport0_mii0_pcs_txd,
   mport0_mii0_pcs_txc, mport0_mac_int, mac_led_logic_chain_valid_out,
   mac_led_logic_chain_data_out, mac_led_logic_chain_code_out,
   mac_led_logic_chain_addr_out, mac_counter_chain_valid_out,
   mac_counter_chain_data_out, mac_counter_chain_code_out,
   mac_counter_chain_addr_out, led_data, led_clk,
   // Inputs
   sys_clk, rst_n, qos_cb_port_pause_eth, pcie_linkstate,
   mport1_time_reg, mport1_speed_mode, mport1_mii_rst_n,
   mport1_mii_clk_781, mport1_mii_clk_625, mport1_mii_clk_390,
   mport1_mii_clk_156, mport1_mii_clk, mport1_mii0_pcs_rxd,
   mport1_mii0_pcs_rxc, mport1_mac_mode, mport1_clk_125,
   mport0_time_reg, mport0_speed_mode, mport0_mii_rst_n,
   mport0_mii_clk_781, mport0_mii_clk_625, mport0_mii_clk_390,
   mport0_mii_clk_156, mport0_mii_clk, mport0_mii0_pcs_rxd,
   mport0_mii0_pcs_rxc, mport0_mac_mode, mport0_clk_125, mac_seed,
   mac_led_logic_chain_valid_in, mac_led_logic_chain_data_in,
   mac_led_logic_chain_code_in, mac_led_logic_chain_addr_in,
   mac_counter_chain_in_valid_in, mac_counter_chain_in_data_in,
   mac_counter_chain_in_code_in, mac_counter_chain_in_addr_in, ecid,
   dice_port9_fifo_wr, dice_port9_data, dice_port8_fifo_wr,
   dice_port8_data, dice_port7_fifo_wr, dice_port7_data,
   dice_port6_fifo_wr, dice_port6_data, dice_port5_fifo_wr,
   dice_port5_data, dice_port4_fifo_wr, dice_port4_data,
   dice_port3_fifo_wr, dice_port3_data, dice_port2_fifo_wr,
   dice_port2_data, dice_port1_fifo_wr, dice_port1_data,
   dice_port15_fifo_wr, dice_port15_data, dice_port14_fifo_wr,
   dice_port14_data, dice_port13_fifo_wr, dice_port13_data,
   dice_port12_fifo_wr, dice_port12_data, dice_port11_fifo_wr,
   dice_port11_data, dice_port10_fifo_wr, dice_port10_data,
   dice_port0_fifo_wr, dice_port0_data, cb_seed
   );
//------------------------auto wire-----------------------------
/*AUTOINPUT*/
// Beginning of automatic inputs (from unused autoinst inputs)
input [63:0]		cb_seed;		// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
input [586:0]		dice_port0_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port0_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port10_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port10_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port11_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port11_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port12_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port12_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port13_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port13_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port14_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port14_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port15_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port15_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port1_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port1_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port2_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port2_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port3_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port3_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port4_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port4_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port5_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port5_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port6_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port6_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port7_data;	// To u0_mac_top of mac_top.v, ...
input			dice_port7_fifo_wr;	// To u0_mac_top of mac_top.v
input [586:0]		dice_port8_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port8_fifo_wr;	// To u1_mac_top of mac_top.v
input [586:0]		dice_port9_data;	// To u1_mac_top of mac_top.v, ...
input			dice_port9_fifo_wr;	// To u1_mac_top of mac_top.v
input [255:0]		ecid;			// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
input [19:0]		mac_counter_chain_in_addr_in;// To u0_mac_top of mac_top.v
input [3:0]		mac_counter_chain_in_code_in;// To u0_mac_top of mac_top.v
input [63:0]		mac_counter_chain_in_data_in;// To u0_mac_top of mac_top.v
input			mac_counter_chain_in_valid_in;// To u0_mac_top of mac_top.v
input [19:0]		mac_led_logic_chain_addr_in;// To u0_mac_top of mac_top.v
input [3:0]		mac_led_logic_chain_code_in;// To u0_mac_top of mac_top.v
input [63:0]		mac_led_logic_chain_data_in;// To u0_mac_top of mac_top.v
input			mac_led_logic_chain_valid_in;// To u0_mac_top of mac_top.v
input [7:0]		mac_seed;		// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
input			mport0_clk_125;		// To u0_mac_top of mac_top.v
input [3:0]		mport0_mac_mode;	// To u0_mac_top of mac_top.v
input [63:0]		mport0_mii0_pcs_rxc;	// To u0_mac_top of mac_top.v
input [511:0]		mport0_mii0_pcs_rxd;	// To u0_mac_top of mac_top.v
input			mport0_mii_clk;		// To u0_mac_top of mac_top.v
input			mport0_mii_clk_156;	// To u0_mac_top of mac_top.v
input			mport0_mii_clk_390;	// To u0_mac_top of mac_top.v
input			mport0_mii_clk_625;	// To u0_mac_top of mac_top.v
input			mport0_mii_clk_781;	// To u0_mac_top of mac_top.v
input			mport0_mii_rst_n;	// To u0_mac_top of mac_top.v
input [3:0]		mport0_speed_mode;	// To u0_mac_top of mac_top.v
input [79:0]		mport0_time_reg;	// To u0_mac_top of mac_top.v
input			mport1_clk_125;		// To u1_mac_top of mac_top.v
input [3:0]		mport1_mac_mode;	// To u1_mac_top of mac_top.v
input [63:0]		mport1_mii0_pcs_rxc;	// To u1_mac_top of mac_top.v
input [511:0]		mport1_mii0_pcs_rxd;	// To u1_mac_top of mac_top.v
input			mport1_mii_clk;		// To u1_mac_top of mac_top.v
input			mport1_mii_clk_156;	// To u1_mac_top of mac_top.v
input			mport1_mii_clk_390;	// To u1_mac_top of mac_top.v
input			mport1_mii_clk_625;	// To u1_mac_top of mac_top.v
input			mport1_mii_clk_781;	// To u1_mac_top of mac_top.v
input			mport1_mii_rst_n;	// To u1_mac_top of mac_top.v
input [3:0]		mport1_speed_mode;	// To u1_mac_top of mac_top.v
input [79:0]		mport1_time_reg;	// To u1_mac_top of mac_top.v
input [(`LED_RANDNUM_PCIE_PORT)-1:0] pcie_linkstate;// To U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
input [15:0]		qos_cb_port_pause_eth;	// To u0_mac_top of mac_top.v, ...
input			rst_n;			// To u0_mac_top of mac_top.v, ...
input			sys_clk;		// To u0_mac_top of mac_top.v, ...
// End of automatics
/*AUTOOUTPUT*/
// Beginning of automatic outputs (from unused autoinst outputs)
output			led_clk;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output			led_data;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output [19:0]		mac_counter_chain_addr_out;// From u1_mac_top of mac_top.v
output [3:0]		mac_counter_chain_code_out;// From u1_mac_top of mac_top.v
output [63:0]		mac_counter_chain_data_out;// From u1_mac_top of mac_top.v
output			mac_counter_chain_valid_out;// From u1_mac_top of mac_top.v
output [19:0]		mac_led_logic_chain_addr_out;// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output [3:0]		mac_led_logic_chain_code_out;// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output [63:0]		mac_led_logic_chain_data_out;// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output			mac_led_logic_chain_valid_out;// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
output			mport0_mac_int;		// From u0_mac_top of mac_top.v
output [63:0]		mport0_mii0_pcs_txc;	// From u0_mac_top of mac_top.v
output [511:0]		mport0_mii0_pcs_txd;	// From u0_mac_top of mac_top.v
output			mport1_mac_int;		// From u1_mac_top of mac_top.v
output [63:0]		mport1_mii0_pcs_txc;	// From u1_mac_top of mac_top.v
output [511:0]		mport1_mii0_pcs_txd;	// From u1_mac_top of mac_top.v
output [31:0]		port0_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port0_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port0_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port0_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port0_slic_data;	// From u0_mac_top of mac_top.v
output			port0_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port10_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port10_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port10_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port10_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port10_slic_data;	// From u1_mac_top of mac_top.v
output			port10_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port11_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port11_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port11_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port11_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port11_slic_data;	// From u1_mac_top of mac_top.v
output			port11_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port12_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port12_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port12_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port12_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port12_slic_data;	// From u1_mac_top of mac_top.v
output			port12_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port13_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port13_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port13_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port13_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port13_slic_data;	// From u1_mac_top of mac_top.v
output			port13_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port14_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port14_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port14_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port14_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port14_slic_data;	// From u1_mac_top of mac_top.v
output			port14_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port15_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port15_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port15_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port15_slic_ctl;	// From u1_mac_top of mac_top.v
output [575:0]		port15_slic_data;	// From u1_mac_top of mac_top.v
output			port15_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port1_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port1_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port1_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port1_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port1_slic_data;	// From u0_mac_top of mac_top.v
output			port1_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port2_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port2_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port2_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port2_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port2_slic_data;	// From u0_mac_top of mac_top.v
output			port2_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port3_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port3_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port3_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port3_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port3_slic_data;	// From u0_mac_top of mac_top.v
output			port3_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port4_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port4_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port4_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port4_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port4_slic_data;	// From u0_mac_top of mac_top.v
output			port4_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port5_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port5_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port5_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port5_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port5_slic_data;	// From u0_mac_top of mac_top.v
output			port5_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port6_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port6_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port6_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port6_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port6_slic_data;	// From u0_mac_top of mac_top.v
output			port6_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port7_dice_1588_timestamp;// From u0_mac_top of mac_top.v
output			port7_dice_1588_valid;	// From u0_mac_top of mac_top.v
output			port7_dice_fifo_free;	// From u0_mac_top of mac_top.v
output [41:0]		port7_slic_ctl;		// From u0_mac_top of mac_top.v
output [575:0]		port7_slic_data;	// From u0_mac_top of mac_top.v
output			port7_slic_data_valid;	// From u0_mac_top of mac_top.v
output [31:0]		port8_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port8_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port8_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port8_slic_ctl;		// From u1_mac_top of mac_top.v
output [575:0]		port8_slic_data;	// From u1_mac_top of mac_top.v
output			port8_slic_data_valid;	// From u1_mac_top of mac_top.v
output [31:0]		port9_dice_1588_timestamp;// From u1_mac_top of mac_top.v
output			port9_dice_1588_valid;	// From u1_mac_top of mac_top.v
output			port9_dice_fifo_free;	// From u1_mac_top of mac_top.v
output [41:0]		port9_slic_ctl;		// From u1_mac_top of mac_top.v
output [575:0]		port9_slic_data;	// From u1_mac_top of mac_top.v
output			port9_slic_data_valid;	// From u1_mac_top of mac_top.v
output			table_ini_done;		// From U_LED_RANDNUM_TOP of LED_RANDNUM_TOP_EMPTY.v
// End of automatics
//autowire
/*{{{*/
/*AUTOWIRE*/
// Beginning of automatic wires (for undeclared instantiated-module outputs)
wire [19:0]		counter_chain_0_addr;	// From u0_mac_top of mac_top.v
wire [3:0]		counter_chain_0_code;	// From u0_mac_top of mac_top.v
wire [63:0]		counter_chain_0_data;	// From u0_mac_top of mac_top.v
wire			counter_chain_0_valid;	// From u0_mac_top of mac_top.v
wire [19:0]		logic_chain_0_addr;	// From u0_mac_top of mac_top.v
wire [3:0]		logic_chain_0_code;	// From u0_mac_top of mac_top.v
wire [63:0]		logic_chain_0_data;	// From u0_mac_top of mac_top.v
wire			logic_chain_0_valid;	// From u0_mac_top of mac_top.v
wire [19:0]		logic_chain_1_addr;	// From u1_mac_top of mac_top.v
wire [3:0]		logic_chain_1_code;	// From u1_mac_top of mac_top.v
wire [63:0]		logic_chain_1_data;	// From u1_mac_top of mac_top.v
wire			logic_chain_1_valid;	// From u1_mac_top of mac_top.v
wire [15:0]		port_linkup;		// From u0_mac_top of mac_top.v, ...
wire [15:0]		portrx_valid;		// From u0_mac_top of mac_top.v, ...
wire [15:0]		porttx_valid;		// From u0_mac_top of mac_top.v, ...
// End of automatics
/*}}}*/
//==============================================================
//Function  : rlm inst
//Arguments : mport
//==============================================================
//mac0_top/*{{{*/
/*mac_top AUTO_TEMPLATE(
    .sys_rst_n                      (rst_n              ),
    .csr_rst_n                      (rst_n              ),
    .clk_125                        (mport@_clk_125     ),
    .mac_mode                       (mport@_mac_mode[]  ),
    .mii0_pcs_rxc                   (mport@_mii0_pcs_rxc[]),
    .mii0_pcs_rxd                   (mport@_mii0_pcs_rxd[]),
    .mii_clk_156                    (mport@_mii_clk_156 ),
    .mii_clk_390                    (mport@_mii_clk_390 ),
    .mii_clk_625                    (mport@_mii_clk_625 ),
    .mii_clk_781                    (mport@_mii_clk_781 ),
    .mii_rst_n                      (mport@_mii_rst_n   ),
    .mii_clk                        (mport@_mii_clk     ),
    .speed_mode                     (mport@_speed_mode[]),
    .time_reg                       (mport@_time_reg[]  ),
    .mac_400g                       (),
    .mii0_pcs_txc                   (mport@_mii0_pcs_txc[]),
    .mii0_pcs_txd                   (mport@_mii0_pcs_txd[]),
	.mac_int			            (mport@_mac_int     ),
    //--------------- nr interface  --------------//
    // ingress fifo interface
    .port_damq0_wen(),
    .port_damq0_wdata(),          //{timestamp(32bit)+ data(576bot)}
    .port_damq0_ctrl(),           //{sop(1bit)+eop(1bit)+err(1bit)+lbo(7bit)}
    
    .port_damq1_wen(),
    .port_damq1_wdata(),          //{timestamp(32bit)+ data(576bot)}
    .port_damq1_ctrl(),           //{sop(1bit)+eop(1bit)+err(1bit)+lbo(7bit)}
    // egress fifo interface
    .port_dice_fifo_free(),
    .dice_port_fifo_data(576'd0),
    .dice_port_fifo_we(4'd0),
    .dice_port_fifo_ctrl(59'd0),

    .reg_chain_valid_in             (mac_led_logic_chain_valid_in    ),
    .reg_chain_code_in              (mac_led_logic_chain_code_in[]   ),
    .reg_chain_addr_in              (mac_led_logic_chain_addr_in[]   ),
    .reg_chain_data_in              (mac_led_logic_chain_data_in[]   ),
    .reg_chain_valid_out            (logic_chain_0_valid   ),
    .reg_chain_code_out             (logic_chain_0_code[]  ),
    .reg_chain_addr_out             (logic_chain_0_addr[]  ),
    .reg_chain_data_out             (logic_chain_0_data[]  ),
                                                               
    .counter_reg_chain_valid_in     (mac_counter_chain_in_valid_in  ),
    .counter_reg_chain_code_in      (mac_counter_chain_in_code_in[] ),
    .counter_reg_chain_addr_in      (mac_counter_chain_in_addr_in[] ),
    .counter_reg_chain_data_in      (mac_counter_chain_in_data_in[] ),
    .counter_reg_chain_valid_out    (counter_chain_0_valid ),
    .counter_reg_chain_code_out     (counter_chain_0_code[]),
    .counter_reg_chain_addr_out     (counter_chain_0_addr[]),
    .counter_reg_chain_data_out     (counter_chain_0_data[]),

    .led0_rx_valid      (portrx_valid[0] ),
    .led0_tx_valid      (porttx_valid[0] ),
    .led0_link_up       (port_linkup[0]  ),

    .led1_rx_valid      (portrx_valid[1] ),
    .led1_tx_valid      (porttx_valid[1] ),
    .led1_link_up       (port_linkup[1]  ),

    .led2_rx_valid      (portrx_valid[2] ),
    .led2_tx_valid      (porttx_valid[2] ),
    .led2_link_up       (port_linkup[2]  ),

    .led3_rx_valid      (portrx_valid[3] ),
    .led3_tx_valid      (porttx_valid[3] ),
    .led3_link_up       (port_linkup[3]  ),

    .led4_rx_valid      (portrx_valid[4] ),
    .led4_tx_valid      (porttx_valid[4] ),
    .led4_link_up       (port_linkup[4]  ),

    .led5_rx_valid      (portrx_valid[5] ),
    .led5_tx_valid      (porttx_valid[5] ),
    .led5_link_up       (port_linkup[5]  ),

    .led6_rx_valid      (portrx_valid[6] ),
    .led6_tx_valid      (porttx_valid[6] ),
    .led6_link_up       (port_linkup[6]  ),

    .led7_rx_valid      (portrx_valid[7] ),
    .led7_tx_valid      (porttx_valid[7] ),
    .led7_link_up       (port_linkup[7]  ),

    //.port_pause         (qos_cb_port_pause_eth[7:0]),

    .qos_port0_pause        ({qos_cb_port_pause_eth[0],8'd0}),   // {pause + pfc}
    .qos_port1_pause        ({qos_cb_port_pause_eth[1],8'd0}),
    .qos_port2_pause        ({qos_cb_port_pause_eth[2],8'd0}),
    .qos_port3_pause        ({qos_cb_port_pause_eth[3],8'd0}),
    .qos_port4_pause        ({qos_cb_port_pause_eth[4],8'd0}),
    .qos_port5_pause        ({qos_cb_port_pause_eth[5],8'd0}),
    .qos_port6_pause        ({qos_cb_port_pause_eth[6],8'd0}),
    .qos_port7_pause        ({qos_cb_port_pause_eth[7],8'd0}),
    
    .port0_dice_pfc_pause   (),   
    .port1_dice_pfc_pause   (),
    .port2_dice_pfc_pause   (),
    .port3_dice_pfc_pause   (),
    .port4_dice_pfc_pause   (),
    .port5_dice_pfc_pause   (),
    .port6_dice_pfc_pause   (),
    .port7_dice_pfc_pause   (),

    .port_slice_fifo0_data  (port0_slic_data[]         ),      //576bit data
    .port_slice_fifo0_ctrl  (port0_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo0_vld   (port0_slic_data_valid     ),
    
    .port_slice_fifo1_data  (port1_slic_data[]         ),      //576bit data
    .port_slice_fifo1_ctrl  (port1_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo1_vld   (port1_slic_data_valid     ),
    
    .port_slice_fifo2_data  (port2_slic_data[]         ),      //576bit data
    .port_slice_fifo2_ctrl  (port2_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo2_vld   (port2_slic_data_valid     ),
    
    .port_slice_fifo3_data  (port3_slic_data[]         ),      //576bit data
    .port_slice_fifo3_ctrl  (port3_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo3_vld   (port3_slic_data_valid     ),

    .port_slice_fifo4_data  (port4_slic_data[]         ),      //576bit data
    .port_slice_fifo4_ctrl  (port4_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo4_vld   (port4_slic_data_valid     ),
    
    .port_slice_fifo5_data  (port5_slic_data[]         ),      //576bit data
    .port_slice_fifo5_ctrl  (port5_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo5_vld   (port5_slic_data_valid     ),
    
    .port_slice_fifo6_data  (port6_slic_data[]         ),      //576bit data
    .port_slice_fifo6_ctrl  (port6_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo6_vld   (port6_slic_data_valid     ),
    
    .port_slice_fifo7_data  (port7_slic_data[]         ),      //576bit data
    .port_slice_fifo7_ctrl  (port7_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo7_vld   (port7_slic_data_valid     ),

    .port_dice_fifo0_free   (port0_dice_fifo_free       ),
    .dice_port_fifo0_data   (dice_port0_data[586:11]    ),
    .dice_port_fifo0_we     (dice_port0_fifo_wr         ),
    .dice_port_fifo0_ctrl   (dice_port0_data[58:0]      ),

    .port_dice_fifo1_free   (port1_dice_fifo_free       ),
    .dice_port_fifo1_data   (dice_port1_data[586:11]    ),
    .dice_port_fifo1_we     (dice_port1_fifo_wr         ),
    .dice_port_fifo1_ctrl   (dice_port1_data[58:0]      ),

    .port_dice_fifo2_free   (port2_dice_fifo_free       ),
    .dice_port_fifo2_data   (dice_port2_data[586:11]    ),
    .dice_port_fifo2_we     (dice_port2_fifo_wr         ),
    .dice_port_fifo2_ctrl   (dice_port2_data[58:0]      ),

    .port_dice_fifo3_free   (port3_dice_fifo_free       ), 
    .dice_port_fifo3_data   (dice_port3_data[586:11]    ),
    .dice_port_fifo3_we     (dice_port3_fifo_wr         ),
    .dice_port_fifo3_ctrl   (dice_port3_data[58:0]      ),

    .port_dice_fifo4_free   (port4_dice_fifo_free       ),
    .dice_port_fifo4_data   (dice_port4_data[586:11]    ),
    .dice_port_fifo4_we     (dice_port4_fifo_wr         ),
    .dice_port_fifo4_ctrl   (dice_port4_data[58:0]      ),

    .port_dice_fifo5_free   (port5_dice_fifo_free       ),
    .dice_port_fifo5_data   (dice_port5_data[586:11]    ),
    .dice_port_fifo5_we     (dice_port5_fifo_wr         ),
    .dice_port_fifo5_ctrl   (dice_port5_data[58:0]      ),

    .port_dice_fifo6_free   (port6_dice_fifo_free       ),
    .dice_port_fifo6_data   (dice_port6_data[586:11]    ),
    .dice_port_fifo6_we     (dice_port6_fifo_wr         ),
    .dice_port_fifo6_ctrl   (dice_port6_data[58:0]      ),

    .port_dice_fifo7_free   (port7_dice_fifo_free       ),
    .dice_port_fifo7_data   (dice_port7_data[586:11]    ),
    .dice_port_fifo7_we     (dice_port7_fifo_wr         ),
    .dice_port_fifo7_ctrl   (dice_port7_data[58:0]      ),

    .port0_1588_valid       (port0_dice_1588_valid      ),
    .port0_1588_time_stamp  (port0_dice_1588_timestamp[]  ),
    .port1_1588_valid       (port1_dice_1588_valid      ),
    .port1_1588_time_stamp  (port1_dice_1588_timestamp[]  ),
    .port2_1588_valid       (port2_dice_1588_valid      ),
    .port2_1588_time_stamp  (port2_dice_1588_timestamp[]  ),
    .port3_1588_valid       (port3_dice_1588_valid      ),
    .port3_1588_time_stamp  (port3_dice_1588_timestamp[]  ),

    .port4_1588_valid       (port4_dice_1588_valid      ),
    .port4_1588_time_stamp  (port4_dice_1588_timestamp[]  ),
    .port5_1588_valid       (port5_dice_1588_valid      ),
    .port5_1588_time_stamp  (port5_dice_1588_timestamp[]  ),
    .port6_1588_valid       (port6_dice_1588_valid      ),
    .port6_1588_time_stamp  (port6_dice_1588_timestamp[]  ),
    .port7_1588_valid       (port7_dice_1588_valid      ),
    .port7_1588_time_stamp  (port7_dice_1588_timestamp[]  ),
);*/
mac_top#(
    .CSR_CHAIN_ADDR_PREFIX          (`MPORT0_MAC_ADDR_PREFIX),
    .COUNTER_CSR_CHAIN_ADDR_PREFIX  (`MPORT0_COUNTER_ADDR_PREFIX),
    .PORT_NUM                       ('d8)
)
    u0_mac_top(/*AUTOINST*/
	       // Outputs
	       .mii0_pcs_txc		(mport0_mii0_pcs_txc[63:0]), // Templated
	       .mii0_pcs_txd		(mport0_mii0_pcs_txd[511:0]), // Templated
	       .port_damq0_wen		(),			 // Templated
	       .port_damq0_wdata	(),			 // Templated
	       .port_damq0_ctrl		(),			 // Templated
	       .port_damq1_wen		(),			 // Templated
	       .port_damq1_wdata	(),			 // Templated
	       .port_damq1_ctrl		(),			 // Templated
	       .port_dice_fifo_free	(),			 // Templated
	       .port_slice_fifo0_data	(port0_slic_data[575:0]         ), // Templated
	       .port_slice_fifo0_ctrl	(port0_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo0_vld	(port0_slic_data_valid     ), // Templated
	       .port_slice_fifo1_data	(port1_slic_data[575:0]         ), // Templated
	       .port_slice_fifo1_ctrl	(port1_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo1_vld	(port1_slic_data_valid     ), // Templated
	       .port_slice_fifo2_data	(port2_slic_data[575:0]         ), // Templated
	       .port_slice_fifo2_ctrl	(port2_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo2_vld	(port2_slic_data_valid     ), // Templated
	       .port_slice_fifo3_data	(port3_slic_data[575:0]         ), // Templated
	       .port_slice_fifo3_ctrl	(port3_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo3_vld	(port3_slic_data_valid     ), // Templated
	       .port_slice_fifo4_data	(port4_slic_data[575:0]         ), // Templated
	       .port_slice_fifo4_ctrl	(port4_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo4_vld	(port4_slic_data_valid     ), // Templated
	       .port_slice_fifo5_data	(port5_slic_data[575:0]         ), // Templated
	       .port_slice_fifo5_ctrl	(port5_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo5_vld	(port5_slic_data_valid     ), // Templated
	       .port_slice_fifo6_data	(port6_slic_data[575:0]         ), // Templated
	       .port_slice_fifo6_ctrl	(port6_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo6_vld	(port6_slic_data_valid     ), // Templated
	       .port_slice_fifo7_data	(port7_slic_data[575:0]         ), // Templated
	       .port_slice_fifo7_ctrl	(port7_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo7_vld	(port7_slic_data_valid     ), // Templated
	       .port_dice_fifo0_free	(port0_dice_fifo_free       ), // Templated
	       .port_dice_fifo1_free	(port1_dice_fifo_free       ), // Templated
	       .port_dice_fifo2_free	(port2_dice_fifo_free       ), // Templated
	       .port_dice_fifo3_free	(port3_dice_fifo_free       ), // Templated
	       .port_dice_fifo4_free	(port4_dice_fifo_free       ), // Templated
	       .port_dice_fifo5_free	(port5_dice_fifo_free       ), // Templated
	       .port_dice_fifo6_free	(port6_dice_fifo_free       ), // Templated
	       .port_dice_fifo7_free	(port7_dice_fifo_free       ), // Templated
	       .port0_1588_valid	(port0_dice_1588_valid      ), // Templated
	       .port0_1588_time_stamp	(port0_dice_1588_timestamp[31:0]  ), // Templated
	       .port1_1588_valid	(port1_dice_1588_valid      ), // Templated
	       .port1_1588_time_stamp	(port1_dice_1588_timestamp[31:0]  ), // Templated
	       .port2_1588_valid	(port2_dice_1588_valid      ), // Templated
	       .port2_1588_time_stamp	(port2_dice_1588_timestamp[31:0]  ), // Templated
	       .port3_1588_valid	(port3_dice_1588_valid      ), // Templated
	       .port3_1588_time_stamp	(port3_dice_1588_timestamp[31:0]  ), // Templated
	       .port4_1588_valid	(port4_dice_1588_valid      ), // Templated
	       .port4_1588_time_stamp	(port4_dice_1588_timestamp[31:0]  ), // Templated
	       .port5_1588_valid	(port5_dice_1588_valid      ), // Templated
	       .port5_1588_time_stamp	(port5_dice_1588_timestamp[31:0]  ), // Templated
	       .port6_1588_valid	(port6_dice_1588_valid      ), // Templated
	       .port6_1588_time_stamp	(port6_dice_1588_timestamp[31:0]  ), // Templated
	       .port7_1588_valid	(port7_dice_1588_valid      ), // Templated
	       .port7_1588_time_stamp	(port7_dice_1588_timestamp[31:0]  ), // Templated
	       .reg_chain_valid_out	(logic_chain_0_valid   ), // Templated
	       .reg_chain_code_out	(logic_chain_0_code[3:0]  ), // Templated
	       .reg_chain_addr_out	(logic_chain_0_addr[19:0]  ), // Templated
	       .reg_chain_data_out	(logic_chain_0_data[63:0]  ), // Templated
	       .counter_reg_chain_addr_out(counter_chain_0_addr[19:0]), // Templated
	       .counter_reg_chain_code_out(counter_chain_0_code[3:0]), // Templated
	       .counter_reg_chain_data_out(counter_chain_0_data[63:0]), // Templated
	       .counter_reg_chain_valid_out(counter_chain_0_valid ), // Templated
	       .port0_dice_pfc_pause	(),			 // Templated
	       .port1_dice_pfc_pause	(),			 // Templated
	       .port2_dice_pfc_pause	(),			 // Templated
	       .port3_dice_pfc_pause	(),			 // Templated
	       .port4_dice_pfc_pause	(),			 // Templated
	       .port5_dice_pfc_pause	(),			 // Templated
	       .port6_dice_pfc_pause	(),			 // Templated
	       .port7_dice_pfc_pause	(),			 // Templated
	       .mac_400g		(),			 // Templated
	       .mac_int			(mport0_mac_int     ),	 // Templated
	       .led0_rx_valid		(portrx_valid[0] ),	 // Templated
	       .led0_tx_valid		(porttx_valid[0] ),	 // Templated
	       .led0_link_up		(port_linkup[0]  ),	 // Templated
	       .led1_rx_valid		(portrx_valid[1] ),	 // Templated
	       .led1_tx_valid		(porttx_valid[1] ),	 // Templated
	       .led1_link_up		(port_linkup[1]  ),	 // Templated
	       .led2_rx_valid		(portrx_valid[2] ),	 // Templated
	       .led2_tx_valid		(porttx_valid[2] ),	 // Templated
	       .led2_link_up		(port_linkup[2]  ),	 // Templated
	       .led3_rx_valid		(portrx_valid[3] ),	 // Templated
	       .led3_tx_valid		(porttx_valid[3] ),	 // Templated
	       .led3_link_up		(port_linkup[3]  ),	 // Templated
	       .led4_rx_valid		(portrx_valid[4] ),	 // Templated
	       .led4_tx_valid		(porttx_valid[4] ),	 // Templated
	       .led4_link_up		(port_linkup[4]  ),	 // Templated
	       .led5_rx_valid		(portrx_valid[5] ),	 // Templated
	       .led5_tx_valid		(porttx_valid[5] ),	 // Templated
	       .led5_link_up		(port_linkup[5]  ),	 // Templated
	       .led6_rx_valid		(portrx_valid[6] ),	 // Templated
	       .led6_tx_valid		(porttx_valid[6] ),	 // Templated
	       .led6_link_up		(port_linkup[6]  ),	 // Templated
	       .led7_rx_valid		(portrx_valid[7] ),	 // Templated
	       .led7_tx_valid		(porttx_valid[7] ),	 // Templated
	       .led7_link_up		(port_linkup[7]  ),	 // Templated
	       // Inputs
	       .csr_rst_n		(rst_n              ),	 // Templated
	       .sys_rst_n		(rst_n              ),	 // Templated
	       .sys_clk			(sys_clk),
	       .clk_125			(mport0_clk_125     ),	 // Templated
	       .mii_rst_n		(mport0_mii_rst_n   ),	 // Templated
	       .mii_clk_781		(mport0_mii_clk_781 ),	 // Templated
	       .mii_clk_625		(mport0_mii_clk_625 ),	 // Templated
	       .mii_clk_390		(mport0_mii_clk_390 ),	 // Templated
	       .mii_clk_156		(mport0_mii_clk_156 ),	 // Templated
	       .mii_clk			(mport0_mii_clk     ),	 // Templated
	       .mii0_pcs_rxc		(mport0_mii0_pcs_rxc[63:0]), // Templated
	       .mii0_pcs_rxd		(mport0_mii0_pcs_rxd[511:0]), // Templated
	       .dice_port_fifo_data	(576'd0),		 // Templated
	       .dice_port_fifo_we	(4'd0),			 // Templated
	       .dice_port_fifo_ctrl	(59'd0),		 // Templated
	       .dice_port_fifo0_data	(dice_port0_data[586:11]    ), // Templated
	       .dice_port_fifo0_we	(dice_port0_fifo_wr         ), // Templated
	       .dice_port_fifo0_ctrl	(dice_port0_data[58:0]      ), // Templated
	       .dice_port_fifo1_data	(dice_port1_data[586:11]    ), // Templated
	       .dice_port_fifo1_we	(dice_port1_fifo_wr         ), // Templated
	       .dice_port_fifo1_ctrl	(dice_port1_data[58:0]      ), // Templated
	       .dice_port_fifo2_data	(dice_port2_data[586:11]    ), // Templated
	       .dice_port_fifo2_we	(dice_port2_fifo_wr         ), // Templated
	       .dice_port_fifo2_ctrl	(dice_port2_data[58:0]      ), // Templated
	       .dice_port_fifo3_data	(dice_port3_data[586:11]    ), // Templated
	       .dice_port_fifo3_we	(dice_port3_fifo_wr         ), // Templated
	       .dice_port_fifo3_ctrl	(dice_port3_data[58:0]      ), // Templated
	       .dice_port_fifo4_data	(dice_port4_data[586:11]    ), // Templated
	       .dice_port_fifo4_we	(dice_port4_fifo_wr         ), // Templated
	       .dice_port_fifo4_ctrl	(dice_port4_data[58:0]      ), // Templated
	       .dice_port_fifo5_data	(dice_port5_data[586:11]    ), // Templated
	       .dice_port_fifo5_we	(dice_port5_fifo_wr         ), // Templated
	       .dice_port_fifo5_ctrl	(dice_port5_data[58:0]      ), // Templated
	       .dice_port_fifo6_data	(dice_port6_data[586:11]    ), // Templated
	       .dice_port_fifo6_we	(dice_port6_fifo_wr         ), // Templated
	       .dice_port_fifo6_ctrl	(dice_port6_data[58:0]      ), // Templated
	       .dice_port_fifo7_data	(dice_port7_data[586:11]    ), // Templated
	       .dice_port_fifo7_we	(dice_port7_fifo_wr         ), // Templated
	       .dice_port_fifo7_ctrl	(dice_port7_data[58:0]      ), // Templated
	       .reg_chain_valid_in	(mac_led_logic_chain_valid_in    ), // Templated
	       .reg_chain_code_in	(mac_led_logic_chain_code_in[3:0]   ), // Templated
	       .reg_chain_addr_in	(mac_led_logic_chain_addr_in[19:0]   ), // Templated
	       .reg_chain_data_in	(mac_led_logic_chain_data_in[63:0]   ), // Templated
	       .counter_reg_chain_addr_in(mac_counter_chain_in_addr_in[19:0] ), // Templated
	       .counter_reg_chain_code_in(mac_counter_chain_in_code_in[3:0] ), // Templated
	       .counter_reg_chain_data_in(mac_counter_chain_in_data_in[63:0] ), // Templated
	       .counter_reg_chain_valid_in(mac_counter_chain_in_valid_in  ), // Templated
	       .speed_mode		(mport0_speed_mode[3:0]), // Templated
	       .mac_mode		(mport0_mac_mode[3:0]  ), // Templated
	       .qos_port0_pause		({qos_cb_port_pause_eth[0],8'd0}), // Templated
	       .qos_port1_pause		({qos_cb_port_pause_eth[1],8'd0}), // Templated
	       .qos_port2_pause		({qos_cb_port_pause_eth[2],8'd0}), // Templated
	       .qos_port3_pause		({qos_cb_port_pause_eth[3],8'd0}), // Templated
	       .qos_port4_pause		({qos_cb_port_pause_eth[4],8'd0}), // Templated
	       .qos_port5_pause		({qos_cb_port_pause_eth[5],8'd0}), // Templated
	       .qos_port6_pause		({qos_cb_port_pause_eth[6],8'd0}), // Templated
	       .qos_port7_pause		({qos_cb_port_pause_eth[7],8'd0}), // Templated
	       .time_reg		(mport0_time_reg[79:0]  )); // Templated
/*}}}*/

//mac1_top/*{{{*/
/*mac_top AUTO_TEMPLATE(
    .sys_rst_n                      (rst_n              ),
    .csr_rst_n                      (rst_n              ),
    .clk_125                        (mport@_clk_125     ),
    .mac_mode                       (mport@_mac_mode[]  ),
    .mii0_pcs_rxc                   (mport@_mii0_pcs_rxc[]),
    .mii0_pcs_rxd                   (mport@_mii0_pcs_rxd[]),
    .mii_clk_156                    (mport@_mii_clk_156 ),
    .mii_clk_390                    (mport@_mii_clk_390 ),
    .mii_clk_625                    (mport@_mii_clk_625 ),
    .mii_clk_781                    (mport@_mii_clk_781 ),
    .mii_rst_n                      (mport@_mii_rst_n   ),
    .mii_clk                        (mport@_mii_clk     ),
    .speed_mode                     (mport@_speed_mode[]),
    .time_reg                       (mport@_time_reg[]  ),
    .mac_400g                       (),
    .mii0_pcs_txc                   (mport@_mii0_pcs_txc[]),
    .mii0_pcs_txd                   (mport@_mii0_pcs_txd[]),
	.mac_int			            (mport@_mac_int     ),
    //--------------- nr interface  --------------//
    // ingress fifo interface
    .port_damq0_wen(),
    .port_damq0_wdata(),          //{timestamp(32bit)+ data(576bot)}
    .port_damq0_ctrl(),           //{sop(1bit)+eop(1bit)+err(1bit)+lbo(7bit)}
    
    .port_damq1_wen(),
    .port_damq1_wdata(),          //{timestamp(32bit)+ data(576bot)}
    .port_damq1_ctrl(),           //{sop(1bit)+eop(1bit)+err(1bit)+lbo(7bit)}
    // egress fifo interface
    .port_dice_fifo_free(),
    .dice_port_fifo_data(576'd0),
    .dice_port_fifo_we(4'd0),
    .dice_port_fifo_ctrl(59'd0),

    .reg_chain_valid_in             (logic_chain_0_valid   ),
    .reg_chain_code_in              (logic_chain_0_code[]  ),
    .reg_chain_addr_in              (logic_chain_0_addr[]  ),
    .reg_chain_data_in              (logic_chain_0_data[]  ),
    .reg_chain_valid_out            (logic_chain_1_valid   ),
    .reg_chain_code_out             (logic_chain_1_code[]  ),
    .reg_chain_addr_out             (logic_chain_1_addr[]  ),
    .reg_chain_data_out             (logic_chain_1_data[]  ),
                                                               
    .counter_reg_chain_valid_in     (counter_chain_0_valid  ),
    .counter_reg_chain_code_in      (counter_chain_0_code[] ),
    .counter_reg_chain_addr_in      (counter_chain_0_addr[] ),
    .counter_reg_chain_data_in      (counter_chain_0_data[] ),
    .counter_reg_chain_valid_out    (mac_counter_chain_valid_out ),
    .counter_reg_chain_code_out     (mac_counter_chain_code_out[]),
    .counter_reg_chain_addr_out     (mac_counter_chain_addr_out[]),
    .counter_reg_chain_data_out     (mac_counter_chain_data_out[]),


    .led0_rx_valid      (portrx_valid[8] ),
    .led0_tx_valid      (porttx_valid[8] ),
    .led0_link_up       (port_linkup[8]  ),

    .led1_rx_valid      (portrx_valid[9] ),
    .led1_tx_valid      (porttx_valid[9] ),
    .led1_link_up       (port_linkup[9]  ),

    .led2_rx_valid      (portrx_valid[10] ),
    .led2_tx_valid      (porttx_valid[10] ),
    .led2_link_up       (port_linkup[10]  ),

    .led3_rx_valid      (portrx_valid[11] ),
    .led3_tx_valid      (porttx_valid[11] ),
    .led3_link_up       (port_linkup[11]  ),

    .led4_rx_valid      (portrx_valid[12] ),
    .led4_tx_valid      (porttx_valid[12] ),
    .led4_link_up       (port_linkup[12]  ),

    .led5_rx_valid      (portrx_valid[13] ),
    .led5_tx_valid      (porttx_valid[13] ),
    .led5_link_up       (port_linkup[13]  ),

    .led6_rx_valid      (portrx_valid[14] ),
    .led6_tx_valid      (porttx_valid[14] ),
    .led6_link_up       (port_linkup[14]  ),

    .led7_rx_valid      (portrx_valid[15] ),
    .led7_tx_valid      (porttx_valid[15] ),
    .led7_link_up       (port_linkup[15]  ),

    //.port_pause         (qos_cb_port_pause_eth[7:0]),

    .qos_port0_pause        ({qos_cb_port_pause_eth[8],8'd0}),   // {pause + pfc}
    .qos_port1_pause        ({qos_cb_port_pause_eth[9],8'd0}),
    .qos_port2_pause        ({qos_cb_port_pause_eth[10],8'd0}),
    .qos_port3_pause        ({qos_cb_port_pause_eth[11],8'd0}),
    .qos_port4_pause        ({qos_cb_port_pause_eth[12],8'd0}),
    .qos_port5_pause        ({qos_cb_port_pause_eth[13],8'd0}),
    .qos_port6_pause        ({qos_cb_port_pause_eth[14],8'd0}),
    .qos_port7_pause        ({qos_cb_port_pause_eth[15],8'd0}),
    
    .port0_dice_pfc_pause   (),   
    .port1_dice_pfc_pause   (),
    .port2_dice_pfc_pause   (),
    .port3_dice_pfc_pause   (),
    .port4_dice_pfc_pause   (),
    .port5_dice_pfc_pause   (),
    .port6_dice_pfc_pause   (),
    .port7_dice_pfc_pause   (),


    .port_slice_fifo0_data  (port8_slic_data[]         ),      //576bit data
    .port_slice_fifo0_ctrl  (port8_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo0_vld   (port8_slic_data_valid     ),
    
    .port_slice_fifo1_data  (port9_slic_data[]         ),      //576bit data
    .port_slice_fifo1_ctrl  (port9_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo1_vld   (port9_slic_data_valid     ),
    
    .port_slice_fifo2_data  (port10_slic_data[]         ),      //576bit data
    .port_slice_fifo2_ctrl  (port10_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo2_vld   (port10_slic_data_valid     ),
    
    .port_slice_fifo3_data  (port11_slic_data[]         ),      //576bit data
    .port_slice_fifo3_ctrl  (port11_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo3_vld   (port11_slic_data_valid     ),

    .port_slice_fifo4_data  (port12_slic_data[]         ),      //576bit data
    .port_slice_fifo4_ctrl  (port12_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo4_vld   (port12_slic_data_valid     ),
    
    .port_slice_fifo5_data  (port13_slic_data[]         ),      //576bit data
    .port_slice_fifo5_ctrl  (port13_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo5_vld   (port13_slic_data_valid     ),
    
    .port_slice_fifo6_data  (port14_slic_data[]         ),      //576bit data
    .port_slice_fifo6_ctrl  (port14_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo6_vld   (port14_slic_data_valid     ),
    
    .port_slice_fifo7_data  (port15_slic_data[]         ),      //576bit data
    .port_slice_fifo7_ctrl  (port15_slic_ctl[]          ),     //{ctrl(32bit)+lbo(7bit)+err(1bit)+eop(1bit)+sop(1bit)}
    .port_slice_fifo7_vld   (port15_slic_data_valid     ),

    .port_dice_fifo0_free   (port8_dice_fifo_free       ),
    .dice_port_fifo0_data   (dice_port8_data[586:11]    ),
    .dice_port_fifo0_we     (dice_port8_fifo_wr         ),
    .dice_port_fifo0_ctrl   (dice_port8_data[58:0]      ),

    .port_dice_fifo1_free   (port9_dice_fifo_free       ),
    .dice_port_fifo1_data   (dice_port9_data[586:11]    ),
    .dice_port_fifo1_we     (dice_port9_fifo_wr         ),
    .dice_port_fifo1_ctrl   (dice_port9_data[58:0]      ),

    .port_dice_fifo2_free   (port10_dice_fifo_free       ),
    .dice_port_fifo2_data   (dice_port10_data[586:11]    ),
    .dice_port_fifo2_we     (dice_port10_fifo_wr         ),
    .dice_port_fifo2_ctrl   (dice_port10_data[58:0]      ),

    .port_dice_fifo3_free   (port11_dice_fifo_free       ), 
    .dice_port_fifo3_data   (dice_port11_data[586:11]    ),
    .dice_port_fifo3_we     (dice_port11_fifo_wr         ),
    .dice_port_fifo3_ctrl   (dice_port11_data[58:0]      ),

    .port_dice_fifo4_free   (port12_dice_fifo_free       ),
    .dice_port_fifo4_data   (dice_port12_data[586:11]    ),
    .dice_port_fifo4_we     (dice_port12_fifo_wr         ),
    .dice_port_fifo4_ctrl   (dice_port12_data[58:0]      ),

    .port_dice_fifo5_free   (port13_dice_fifo_free       ),
    .dice_port_fifo5_data   (dice_port13_data[586:11]    ),
    .dice_port_fifo5_we     (dice_port13_fifo_wr         ),
    .dice_port_fifo5_ctrl   (dice_port13_data[58:0]      ),

    .port_dice_fifo6_free   (port14_dice_fifo_free       ),
    .dice_port_fifo6_data   (dice_port14_data[586:11]    ),
    .dice_port_fifo6_we     (dice_port14_fifo_wr         ),
    .dice_port_fifo6_ctrl   (dice_port14_data[58:0]      ),

    .port_dice_fifo7_free   (port15_dice_fifo_free       ),
    .dice_port_fifo7_data   (dice_port15_data[586:11]    ),
    .dice_port_fifo7_we     (dice_port15_fifo_wr         ),
    .dice_port_fifo7_ctrl   (dice_port15_data[58:0]      ),

    .port0_1588_valid       (port8_dice_1588_valid      ),
    .port0_1588_time_stamp  (port8_dice_1588_timestamp[]  ),
    .port1_1588_valid       (port9_dice_1588_valid      ),
    .port1_1588_time_stamp  (port9_dice_1588_timestamp[]  ),
    .port2_1588_valid       (port10_dice_1588_valid      ),
    .port2_1588_time_stamp  (port10_dice_1588_timestamp[]  ),
    .port3_1588_valid       (port11_dice_1588_valid      ),
    .port3_1588_time_stamp  (port11_dice_1588_timestamp[]  ),

    .port4_1588_valid       (port12_dice_1588_valid      ),
    .port4_1588_time_stamp  (port12_dice_1588_timestamp[]  ),
    .port5_1588_valid       (port13_dice_1588_valid      ),
    .port5_1588_time_stamp  (port13_dice_1588_timestamp[]  ),
    .port6_1588_valid       (port14_dice_1588_valid      ),
    .port6_1588_time_stamp  (port14_dice_1588_timestamp[]  ),
    .port7_1588_valid       (port15_dice_1588_valid      ),
    .port7_1588_time_stamp  (port15_dice_1588_timestamp[]  ),
);*/
mac_top#(
    .CSR_CHAIN_ADDR_PREFIX          (`MPORT0_MAC_ADDR_PREFIX),
    .COUNTER_CSR_CHAIN_ADDR_PREFIX  (`MPORT0_COUNTER_ADDR_PREFIX),    
    .PORT_NUM                       ('d8)
)
    u1_mac_top(/*AUTOINST*/
	       // Outputs
	       .mii0_pcs_txc		(mport1_mii0_pcs_txc[63:0]), // Templated
	       .mii0_pcs_txd		(mport1_mii0_pcs_txd[511:0]), // Templated
	       .port_damq0_wen		(),			 // Templated
	       .port_damq0_wdata	(),			 // Templated
	       .port_damq0_ctrl		(),			 // Templated
	       .port_damq1_wen		(),			 // Templated
	       .port_damq1_wdata	(),			 // Templated
	       .port_damq1_ctrl		(),			 // Templated
	       .port_dice_fifo_free	(),			 // Templated
	       .port_slice_fifo0_data	(port8_slic_data[575:0]         ), // Templated
	       .port_slice_fifo0_ctrl	(port8_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo0_vld	(port8_slic_data_valid     ), // Templated
	       .port_slice_fifo1_data	(port9_slic_data[575:0]         ), // Templated
	       .port_slice_fifo1_ctrl	(port9_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo1_vld	(port9_slic_data_valid     ), // Templated
	       .port_slice_fifo2_data	(port10_slic_data[575:0]         ), // Templated
	       .port_slice_fifo2_ctrl	(port10_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo2_vld	(port10_slic_data_valid     ), // Templated
	       .port_slice_fifo3_data	(port11_slic_data[575:0]         ), // Templated
	       .port_slice_fifo3_ctrl	(port11_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo3_vld	(port11_slic_data_valid     ), // Templated
	       .port_slice_fifo4_data	(port12_slic_data[575:0]         ), // Templated
	       .port_slice_fifo4_ctrl	(port12_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo4_vld	(port12_slic_data_valid     ), // Templated
	       .port_slice_fifo5_data	(port13_slic_data[575:0]         ), // Templated
	       .port_slice_fifo5_ctrl	(port13_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo5_vld	(port13_slic_data_valid     ), // Templated
	       .port_slice_fifo6_data	(port14_slic_data[575:0]         ), // Templated
	       .port_slice_fifo6_ctrl	(port14_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo6_vld	(port14_slic_data_valid     ), // Templated
	       .port_slice_fifo7_data	(port15_slic_data[575:0]         ), // Templated
	       .port_slice_fifo7_ctrl	(port15_slic_ctl[41:0]          ), // Templated
	       .port_slice_fifo7_vld	(port15_slic_data_valid     ), // Templated
	       .port_dice_fifo0_free	(port8_dice_fifo_free       ), // Templated
	       .port_dice_fifo1_free	(port9_dice_fifo_free       ), // Templated
	       .port_dice_fifo2_free	(port10_dice_fifo_free       ), // Templated
	       .port_dice_fifo3_free	(port11_dice_fifo_free       ), // Templated
	       .port_dice_fifo4_free	(port12_dice_fifo_free       ), // Templated
	       .port_dice_fifo5_free	(port13_dice_fifo_free       ), // Templated
	       .port_dice_fifo6_free	(port14_dice_fifo_free       ), // Templated
	       .port_dice_fifo7_free	(port15_dice_fifo_free       ), // Templated
	       .port0_1588_valid	(port8_dice_1588_valid      ), // Templated
	       .port0_1588_time_stamp	(port8_dice_1588_timestamp[31:0]  ), // Templated
	       .port1_1588_valid	(port9_dice_1588_valid      ), // Templated
	       .port1_1588_time_stamp	(port9_dice_1588_timestamp[31:0]  ), // Templated
	       .port2_1588_valid	(port10_dice_1588_valid      ), // Templated
	       .port2_1588_time_stamp	(port10_dice_1588_timestamp[31:0]  ), // Templated
	       .port3_1588_valid	(port11_dice_1588_valid      ), // Templated
	       .port3_1588_time_stamp	(port11_dice_1588_timestamp[31:0]  ), // Templated
	       .port4_1588_valid	(port12_dice_1588_valid      ), // Templated
	       .port4_1588_time_stamp	(port12_dice_1588_timestamp[31:0]  ), // Templated
	       .port5_1588_valid	(port13_dice_1588_valid      ), // Templated
	       .port5_1588_time_stamp	(port13_dice_1588_timestamp[31:0]  ), // Templated
	       .port6_1588_valid	(port14_dice_1588_valid      ), // Templated
	       .port6_1588_time_stamp	(port14_dice_1588_timestamp[31:0]  ), // Templated
	       .port7_1588_valid	(port15_dice_1588_valid      ), // Templated
	       .port7_1588_time_stamp	(port15_dice_1588_timestamp[31:0]  ), // Templated
	       .reg_chain_valid_out	(logic_chain_1_valid   ), // Templated
	       .reg_chain_code_out	(logic_chain_1_code[3:0]  ), // Templated
	       .reg_chain_addr_out	(logic_chain_1_addr[19:0]  ), // Templated
	       .reg_chain_data_out	(logic_chain_1_data[63:0]  ), // Templated
	       .counter_reg_chain_addr_out(mac_counter_chain_addr_out[19:0]), // Templated
	       .counter_reg_chain_code_out(mac_counter_chain_code_out[3:0]), // Templated
	       .counter_reg_chain_data_out(mac_counter_chain_data_out[63:0]), // Templated
	       .counter_reg_chain_valid_out(mac_counter_chain_valid_out ), // Templated
	       .port0_dice_pfc_pause	(),			 // Templated
	       .port1_dice_pfc_pause	(),			 // Templated
	       .port2_dice_pfc_pause	(),			 // Templated
	       .port3_dice_pfc_pause	(),			 // Templated
	       .port4_dice_pfc_pause	(),			 // Templated
	       .port5_dice_pfc_pause	(),			 // Templated
	       .port6_dice_pfc_pause	(),			 // Templated
	       .port7_dice_pfc_pause	(),			 // Templated
	       .mac_400g		(),			 // Templated
	       .mac_int			(mport1_mac_int     ),	 // Templated
	       .led0_rx_valid		(portrx_valid[8] ),	 // Templated
	       .led0_tx_valid		(porttx_valid[8] ),	 // Templated
	       .led0_link_up		(port_linkup[8]  ),	 // Templated
	       .led1_rx_valid		(portrx_valid[9] ),	 // Templated
	       .led1_tx_valid		(porttx_valid[9] ),	 // Templated
	       .led1_link_up		(port_linkup[9]  ),	 // Templated
	       .led2_rx_valid		(portrx_valid[10] ),	 // Templated
	       .led2_tx_valid		(porttx_valid[10] ),	 // Templated
	       .led2_link_up		(port_linkup[10]  ),	 // Templated
	       .led3_rx_valid		(portrx_valid[11] ),	 // Templated
	       .led3_tx_valid		(porttx_valid[11] ),	 // Templated
	       .led3_link_up		(port_linkup[11]  ),	 // Templated
	       .led4_rx_valid		(portrx_valid[12] ),	 // Templated
	       .led4_tx_valid		(porttx_valid[12] ),	 // Templated
	       .led4_link_up		(port_linkup[12]  ),	 // Templated
	       .led5_rx_valid		(portrx_valid[13] ),	 // Templated
	       .led5_tx_valid		(porttx_valid[13] ),	 // Templated
	       .led5_link_up		(port_linkup[13]  ),	 // Templated
	       .led6_rx_valid		(portrx_valid[14] ),	 // Templated
	       .led6_tx_valid		(porttx_valid[14] ),	 // Templated
	       .led6_link_up		(port_linkup[14]  ),	 // Templated
	       .led7_rx_valid		(portrx_valid[15] ),	 // Templated
	       .led7_tx_valid		(porttx_valid[15] ),	 // Templated
	       .led7_link_up		(port_linkup[15]  ),	 // Templated
	       // Inputs
	       .csr_rst_n		(rst_n              ),	 // Templated
	       .sys_rst_n		(rst_n              ),	 // Templated
	       .sys_clk			(sys_clk),
	       .clk_125			(mport1_clk_125     ),	 // Templated
	       .mii_rst_n		(mport1_mii_rst_n   ),	 // Templated
	       .mii_clk_781		(mport1_mii_clk_781 ),	 // Templated
	       .mii_clk_625		(mport1_mii_clk_625 ),	 // Templated
	       .mii_clk_390		(mport1_mii_clk_390 ),	 // Templated
	       .mii_clk_156		(mport1_mii_clk_156 ),	 // Templated
	       .mii_clk			(mport1_mii_clk     ),	 // Templated
	       .mii0_pcs_rxc		(mport1_mii0_pcs_rxc[63:0]), // Templated
	       .mii0_pcs_rxd		(mport1_mii0_pcs_rxd[511:0]), // Templated
	       .dice_port_fifo_data	(576'd0),		 // Templated
	       .dice_port_fifo_we	(4'd0),			 // Templated
	       .dice_port_fifo_ctrl	(59'd0),		 // Templated
	       .dice_port_fifo0_data	(dice_port8_data[586:11]    ), // Templated
	       .dice_port_fifo0_we	(dice_port8_fifo_wr         ), // Templated
	       .dice_port_fifo0_ctrl	(dice_port8_data[58:0]      ), // Templated
	       .dice_port_fifo1_data	(dice_port9_data[586:11]    ), // Templated
	       .dice_port_fifo1_we	(dice_port9_fifo_wr         ), // Templated
	       .dice_port_fifo1_ctrl	(dice_port9_data[58:0]      ), // Templated
	       .dice_port_fifo2_data	(dice_port10_data[586:11]    ), // Templated
	       .dice_port_fifo2_we	(dice_port10_fifo_wr         ), // Templated
	       .dice_port_fifo2_ctrl	(dice_port10_data[58:0]      ), // Templated
	       .dice_port_fifo3_data	(dice_port11_data[586:11]    ), // Templated
	       .dice_port_fifo3_we	(dice_port11_fifo_wr         ), // Templated
	       .dice_port_fifo3_ctrl	(dice_port11_data[58:0]      ), // Templated
	       .dice_port_fifo4_data	(dice_port12_data[586:11]    ), // Templated
	       .dice_port_fifo4_we	(dice_port12_fifo_wr         ), // Templated
	       .dice_port_fifo4_ctrl	(dice_port12_data[58:0]      ), // Templated
	       .dice_port_fifo5_data	(dice_port13_data[586:11]    ), // Templated
	       .dice_port_fifo5_we	(dice_port13_fifo_wr         ), // Templated
	       .dice_port_fifo5_ctrl	(dice_port13_data[58:0]      ), // Templated
	       .dice_port_fifo6_data	(dice_port14_data[586:11]    ), // Templated
	       .dice_port_fifo6_we	(dice_port14_fifo_wr         ), // Templated
	       .dice_port_fifo6_ctrl	(dice_port14_data[58:0]      ), // Templated
	       .dice_port_fifo7_data	(dice_port15_data[586:11]    ), // Templated
	       .dice_port_fifo7_we	(dice_port15_fifo_wr         ), // Templated
	       .dice_port_fifo7_ctrl	(dice_port15_data[58:0]      ), // Templated
	       .reg_chain_valid_in	(logic_chain_0_valid   ), // Templated
	       .reg_chain_code_in	(logic_chain_0_code[3:0]  ), // Templated
	       .reg_chain_addr_in	(logic_chain_0_addr[19:0]  ), // Templated
	       .reg_chain_data_in	(logic_chain_0_data[63:0]  ), // Templated
	       .counter_reg_chain_addr_in(counter_chain_0_addr[19:0] ), // Templated
	       .counter_reg_chain_code_in(counter_chain_0_code[3:0] ), // Templated
	       .counter_reg_chain_data_in(counter_chain_0_data[63:0] ), // Templated
	       .counter_reg_chain_valid_in(counter_chain_0_valid  ), // Templated
	       .speed_mode		(mport1_speed_mode[3:0]), // Templated
	       .mac_mode		(mport1_mac_mode[3:0]  ), // Templated
	       .qos_port0_pause		({qos_cb_port_pause_eth[8],8'd0}), // Templated
	       .qos_port1_pause		({qos_cb_port_pause_eth[9],8'd0}), // Templated
	       .qos_port2_pause		({qos_cb_port_pause_eth[10],8'd0}), // Templated
	       .qos_port3_pause		({qos_cb_port_pause_eth[11],8'd0}), // Templated
	       .qos_port4_pause		({qos_cb_port_pause_eth[12],8'd0}), // Templated
	       .qos_port5_pause		({qos_cb_port_pause_eth[13],8'd0}), // Templated
	       .qos_port6_pause		({qos_cb_port_pause_eth[14],8'd0}), // Templated
	       .qos_port7_pause		({qos_cb_port_pause_eth[15],8'd0}), // Templated
	       .time_reg		(mport1_time_reg[79:0]  )); // Templated
/*}}}*/
//==============================================================
//Function  : rlm inst
//Arguments : led
//==============================================================
//led/*{{{*/
/*LED_RANDNUM_TOP_EMPTY AUTO_TEMPLATE(
    .mac_smp_clk            (sys_clk                   ),
    .reg_chain_valid_in     (logic_chain_1_valid    ),
    .reg_chain_code_in      (logic_chain_1_code[]   ),
    .reg_chain_addr_in      (logic_chain_1_addr[]   ),
    .reg_chain_data_in      (logic_chain_1_data[]   ),
    .reg_chain_valid_out    (mac_led_logic_chain_valid_out   ),
    .reg_chain_code_out     (mac_led_logic_chain_code_out[]  ),
    .reg_chain_addr_out     (mac_led_logic_chain_addr_out[]  ),
    .reg_chain_data_out     (mac_led_logic_chain_data_out[]  ),

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
LED_RANDNUM_TOP_EMPTY
    U_LED_RANDNUM_TOP(/*AUTOINST*/
		      // Outputs
		      .reg_chain_valid_out(mac_led_logic_chain_valid_out   ), // Templated
		      .reg_chain_code_out(mac_led_logic_chain_code_out[3:0]  ), // Templated
		      .reg_chain_addr_out(mac_led_logic_chain_addr_out[19:0]  ), // Templated
		      .reg_chain_data_out(mac_led_logic_chain_data_out[63:0]  ), // Templated
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
		      .reg_chain_valid_in(logic_chain_1_valid    ), // Templated
		      .reg_chain_code_in(logic_chain_1_code[3:0]   ), // Templated
		      .reg_chain_addr_in(logic_chain_1_addr[19:0]   ), // Templated
		      .reg_chain_data_in(logic_chain_1_data[63:0]   ), // Templated
		      .porttx_valid	(porttx_valid[(`LED_RANDNUM_MAC_PORT)-1:0]),
		      .portrx_valid	(portrx_valid[(`LED_RANDNUM_MAC_PORT)-1:0]),
		      .port_likup	(port_linkup[(`LED_RANDNUM_MAC_PORT)-1:0]), // Templated
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
//verilog-library-files:(
//"~/es8000_hw_code/es9600_hw_code/trunk/asic/design_code/mport/mac_merge/source_code/mac_top.v"
//"~/es8000_hw_code/es9600_hw_code/trunk/asic/design_code/top/source_code/led_randnum/source_code/led_randnum_top_empty.v"
//)
//verilog-library-extensions:(".v" ".h")
//verilog-auto-inst-param-value:t
//End:

