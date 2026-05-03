from logger import *
import re

# Master/Slave
bus_master = 1
bus_slave = 2
# Targets
bus_phy = 3
bus_mac = 4
bus_conn = 5
bus_adapter = 6
bus_som = 7
# Special
bus_gpio = 8 # No counterpart, can self assign...
# Power
bus_powerout = 9
bus_powerin = 10
# Driver/Sink/Source
bus_sink = 11
bus_source = 12



kicad_drivers = ['input','output','unspecified','power_in','power_out',
                'open_collector','open_emitter','no_connect','free','tri_state','bidirectional']



class DriverType:
    kicad_drivers = kicad_drivers
    def __init__(self, name, bus_driver, kicad_driver, connection_list, max_allowed_connections, optional):
        if kicad_driver not in self.kicad_drivers:
            log(log_error, f"Driver is not in kicad drivers: {kicad_driver}")
            exit(-1)
        self.allowed_connection_list = []
        # TODO: Add some checks

        self.name = name
        self.kicad_driver = kicad_driver
        for connection in connection_list:
            self.allowed_connection_list.append(connection)
        self.allow_multi_connections = max_allowed_connections
        self.optional = optional
        self.bus_source = bus_driver

bus_qspi = [
    DriverType('qspi_slave[x].csn[x]', bus_slave, 'input',         ['qspi_master[x].csn[x]'], 1, False),
    DriverType('qspi_slave[x].clk',    bus_slave, 'input',         ['qspi_master[x].clk'], 1, False),
    DriverType('qspi_slave[x].io0',    bus_slave, 'bidirectional', ['qspi_master[x].io0'], 1, False),
    DriverType('qspi_slave[x].io1',    bus_slave, 'bidirectional', ['qspi_master[x].io1'], 1, False),
    DriverType('qspi_slave[x].io2',    bus_slave, 'bidirectional', ['qspi_master[x].io2'], 1, False),
    DriverType('qspi_slave[x].io3',    bus_slave, 'bidirectional', ['qspi_master[x].io3'], 1, False),
    DriverType('qspi_slave[x].rstn',   bus_slave, 'input',         ['qspi_master[x].rstn'], 1, True),
    DriverType('qspi_slave[x].wpn',    bus_slave, 'input',         ['qspi_master[x].wpn'], 1, True),


    DriverType('qspi_master[x].csn[x]',  bus_master, 'output',        ['qspi_slave[x].csn[x]'], 1, False),
    DriverType('qspi_master[x].clk',     bus_master, 'output',        ['qspi_slave[x].clk'], 1, False),
    DriverType('qspi_master[x].io0',     bus_master, 'bidirectional', ['qspi_slave[x].io0'], 1, False),
    DriverType('qspi_master[x].io1',     bus_master, 'bidirectional', ['qspi_slave[x].io1'], 1, False),
    DriverType('qspi_master[x].io2',     bus_master, 'bidirectional', ['qspi_slave[x].io2'], 1, False),
    DriverType('qspi_master[x].io3',     bus_master, 'bidirectional', ['qspi_slave[x].io3'], 1, False),
    DriverType('qspi_master[x].rstn',    bus_slave,  'output',        ['qspi_slave[x].rstn'], 1, True),
    DriverType('qspi_master[x].wpn',     bus_slave,  'output',        ['qspi_slave[x].wpn'], 1, True),
]

bus_octaspi = [
    DriverType('octaspi_slave[x].csn[x]', bus_slave, 'input',         ['octaspi_master[x].csn[x]'], 1, False),
    DriverType('octaspi_slave[x].dqs',    bus_slave, 'input',         ['octaspi_master[x].dqs'], 1, False),
    DriverType('octaspi_slave[x].clk',    bus_slave, 'input',         ['octaspi_master[x].clk'], 1, False),
    DriverType('octaspi_slave[x].io0',    bus_slave, 'bidirectional', ['octaspi_master[x].io0'], 1, False),
    DriverType('octaspi_slave[x].io1',    bus_slave, 'bidirectional', ['octaspi_master[x].io1'], 1, False),
    DriverType('octaspi_slave[x].io2',    bus_slave, 'bidirectional', ['octaspi_master[x].io2'], 1, False),
    DriverType('octaspi_slave[x].io3',    bus_slave, 'bidirectional', ['octaspi_master[x].io3'], 1, False),
    DriverType('octaspi_slave[x].io4',    bus_slave, 'bidirectional', ['octaspi_master[x].io4'], 1, False),
    DriverType('octaspi_slave[x].io5',    bus_slave, 'bidirectional', ['octaspi_master[x].io5'], 1, False),
    DriverType('octaspi_slave[x].io6',    bus_slave, 'bidirectional', ['octaspi_master[x].io6'], 1, False),
    DriverType('octaspi_slave[x].io7',    bus_slave, 'bidirectional', ['octaspi_master[x].io7'], 1, False),
    DriverType('octaspi_slave[x].rstn',   bus_slave, 'input',         ['octaspi_master[x].rstn'], 1, True),

    DriverType('octaspi_master[x].csn[x]',  bus_master, 'output',        ['octaspi_slave[x].csn[x]'], 1, False),
    DriverType('octaspi_master[x].dqs',     bus_master, 'output',        ['octaspi_slave[x].dqs'], 1, False),
    DriverType('octaspi_master[x].clk',     bus_master, 'output',        ['octaspi_slave[x].clk'], 1, False),
    DriverType('octaspi_master[x].io0',     bus_master, 'bidirectional', ['octaspi_slave[x].io0'], 1, False),
    DriverType('octaspi_master[x].io1',     bus_master, 'bidirectional', ['octaspi_slave[x].io1'], 1, False),
    DriverType('octaspi_master[x].io2',     bus_master, 'bidirectional', ['octaspi_slave[x].io2'], 1, False),
    DriverType('octaspi_master[x].io3',     bus_master, 'bidirectional', ['octaspi_slave[x].io3'], 1, False),
    DriverType('octaspi_master[x].io4',     bus_master, 'bidirectional', ['octaspi_slave[x].io4'], 1, False),
    DriverType('octaspi_master[x].io5',     bus_master, 'bidirectional', ['octaspi_slave[x].io5'], 1, False),
    DriverType('octaspi_master[x].io6',     bus_master, 'bidirectional', ['octaspi_slave[x].io6'], 1, False),
    DriverType('octaspi_master[x].io7',     bus_master, 'bidirectional', ['octaspi_slave[x].io7'], 1, False),
    DriverType('octaspi_master[x].rstn',    bus_master, 'output',        ['octaspi_slave[x].rstn'], 1, True),
]

bus_spi = [
    DriverType('spi_master[x].csn[x]', bus_master, 'output', ['spi_slave[x].csn[x]'], 1, False),
    DriverType('spi_master[x].miso',   bus_master, 'input',  ['spi_slave[x].miso'], 1, False),
    DriverType('spi_master[x].mosi',   bus_master, 'output', ['spi_slave[x].mosi'], 1, False),
    DriverType('spi_master[x].sck',    bus_master, 'output', ['spi_slave[x].sck'],  1, False),
    DriverType('spi_master[x].rstn',   bus_master, 'output', ['spi_slave[x].rstn'], 1, True),

    DriverType('spi_slave[x].csn[x]', bus_slave, 'input' , ['spi_master[x].csn[x]'], 1, False),
    DriverType('spi_slave[x].miso',   bus_slave, 'output', ['spi_master[x].miso'], 1, False),
    DriverType('spi_slave[x].mosi',   bus_slave, 'input' , ['spi_master[x].mosi'], 1, False),
    DriverType('spi_slave[x].sck',    bus_slave, 'input' , ['spi_master[x].sck'],  1, False),
    DriverType('spi_slave[x].rstn',   bus_slave, 'input',  ['spi_master[x].rstn'], 1, True),
]

bus_jtag = [
    DriverType('jtag_master[x].tms',       bus_master, 'output', ['jtag_slave[x].tms'], 16, False),
    DriverType('jtag_master[x].tck',       bus_master, 'output', ['jtag_slave[x].tck'], 16, False),
    DriverType('jtag_master[x].mosi',      bus_master, 'output', ['jtag_slave[x].tdi'], 1, False),
    DriverType('jtag_master[x].miso',      bus_master, 'input',  ['jtag_slave[x].tdo'], 1, False),
    DriverType('jtag_master[x].trst_n',    bus_master, 'output', ['jtag_slave[x].trst_n'], 1, False),
    DriverType('jtag_master[x].sysrst_n',  bus_master, 'output', ['jtag_slave[x].sysrst_n'], 1, False),

    DriverType('jtag_slave[x].tms',     bus_slave, 'input',  ['jtag_master[x].tms'],  1, False),
    DriverType('jtag_slave[x].tck',     bus_slave, 'input',  ['jtag_master[x].tck'],  1, False),
    DriverType('jtag_slave[x].tdo',     bus_slave, 'output', ['jtag_master[x].miso'], 1, False),
    DriverType('jtag_slave[x].tdi',     bus_slave, 'input',  ['jtag_master[x].mosi'], 1, False),
    DriverType('jtag_slave[x].trstn',   bus_slave, 'input',  ['jtag_master[x].trstn'], 1, False),
    DriverType('jtag_slave[x].sysrstn', bus_slave, 'output', ['jtag_master[x].sysrstn'], 1, False),
]

bus_adapter40p = [
    DriverType('adapter40p_adapter[x].dp0',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dp0'], 1, False),
    DriverType('adapter40p_adapter[x].dp1',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dp1'], 1, False),
    DriverType('adapter40p_adapter[x].dp2',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dp2'], 1, False),
    DriverType('adapter40p_adapter[x].dp3',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dp3'], 1, False),
    DriverType('adapter40p_adapter[x].dn0',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dn0'], 1, False),
    DriverType('adapter40p_adapter[x].dn1',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dn1'], 1, False),
    DriverType('adapter40p_adapter[x].dn2',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dn2'], 1, False),
    DriverType('adapter40p_adapter[x].dn3',     bus_adapter, 'bidirectional', ['adapter40p_som[x].dn3'], 1, False),
    DriverType('adapter40p_adapter[x].a2s_irq', bus_adapter, 'output',        ['adapter40p_som[x].a2s_irq'], 1, False),
    DriverType('adapter40p_adapter[x].s2a_irq', bus_adapter, 'input',         ['adapter40p_som[x].s2a_irq'], 1, False),
    DriverType('adapter40p_adapter[x].clkp',    bus_adapter, 'bidirectional', ['adapter40p_som[x].clkp'   ], 1, False),
    DriverType('adapter40p_adapter[x].clkn',    bus_adapter, 'bidirectional', ['adapter40p_som[x].clkn'   ], 1, False),

    DriverType('adapter40p_som[x].dp0',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dp0'], 1, False),
    DriverType('adapter40p_som[x].dp1',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dp1'], 1, False),
    DriverType('adapter40p_som[x].dp2',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dp2'], 1, False),
    DriverType('adapter40p_som[x].dp3',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dp3'], 1, False),
    DriverType('adapter40p_som[x].dn0',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dn0'], 1, False),
    DriverType('adapter40p_som[x].dn1',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dn1'], 1, False),
    DriverType('adapter40p_som[x].dn2',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dn2'], 1, False),
    DriverType('adapter40p_som[x].dn3',     bus_som, 'bidirectional', ['adapter40p_adapter[x].dn3'], 1, False),
    DriverType('adapter40p_som[x].a2s_irq', bus_som, 'input',         ['adapter40p_adapter[x].a2s_irq'], 1, False),
    DriverType('adapter40p_som[x].s2a_irq', bus_som, 'output',        ['adapter40p_adapter[x].s2a_irq'], 1, False),
    DriverType('adapter40p_som[x].clkp',    bus_som, 'bidirectional', ['adapter40p_adapter[x].clkp'   ], 1, False),
    DriverType('adapter40p_som[x].clkn',    bus_som, 'bidirectional', ['adapter40p_adapter[x].clkn'   ], 1, False),

]

# NOTE:
bus_usart = [
    DriverType('usart_master[x].tx', bus_master, 'output', ['usart_slave[x].rx'], 32, False),
    DriverType('usart_master[x].rx', bus_master, 'input',  ['usart_slave[x].tx'], 32, True),

    DriverType('usart_slave[x].rx',  bus_slave,  'input',  ['usart_master[x].tx'], 1, False),
    DriverType('usart_slave[x].tx',  bus_slave,  'output', ['usart_master[x].rx'], 1, True),
    # TODO: Missing drivers
]

bus_i2c = [
    DriverType('i2c_master[x].sda', bus_master, 'bidirectional', ['i2c_slave[x].sda'], 32, False),
    DriverType('i2c_master[x].scl', bus_master, 'output',        ['i2c_slave[x].scl'], 32, False),
    DriverType('i2c_slave[x].sda',  bus_slave,  'bidirectional', ['i2c_master[x].sda'], 1, False),
    DriverType('i2c_slave[x].scl',  bus_slave,  'output',        ['i2c_master[x].scl'], 1, False),
]

bus_serialwire = [
    DriverType('serialwire_master[x].clk', bus_master, 'output',        ['serialwire_slave[x].clk'],  1, False),
    DriverType('serialwire_master[x].dio', bus_master, 'bidirectional', ['serialwire_slave[x].dio'],  1, False),
    DriverType('serialwire_slave[x].clk',  bus_slave,  'input',         ['serialwire_master[x].clk'], 1, False),
    DriverType('serialwire_slave[x].dio',  bus_slave,  'bidirectional', ['serialwire_master[x].dio'], 1, False),
]

bus_rgmii = [
    DriverType('rgmii_phy[x].txc',    bus_phy, 'input',  ['rgmii_mac[x].txc'], 1, False),
    DriverType('rgmii_phy[x].tx_ctl', bus_phy, 'input',  ['rgmii_mac[x].tx_ctl'], 1, False),
    DriverType('rgmii_phy[x].txd0',   bus_phy, 'input',  ['rgmii_mac[x].txd0'], 1, False),
    DriverType('rgmii_phy[x].txd1',   bus_phy, 'input',  ['rgmii_mac[x].txd1'], 1, False),
    DriverType('rgmii_phy[x].txd2',   bus_phy, 'input',  ['rgmii_mac[x].txd2'], 1, False),
    DriverType('rgmii_phy[x].txd3',   bus_phy, 'input',  ['rgmii_mac[x].txd3'], 1, False),
    DriverType('rgmii_phy[x].rxc',    bus_phy, 'output', ['rgmii_mac[x].rxc'], 1, False),
    DriverType('rgmii_phy[x].rx_ctl', bus_phy, 'output', ['rgmii_mac[x].rx_ctl'], 1, False),
    DriverType('rgmii_phy[x].rxd0',   bus_phy, 'output', ['rgmii_mac[x].rxd0'], 1, False),
    DriverType('rgmii_phy[x].rxd1',   bus_phy, 'output', ['rgmii_mac[x].rxd1'], 1, False),
    DriverType('rgmii_phy[x].rxd2',   bus_phy, 'output', ['rgmii_mac[x].rxd2'], 1, False),
    DriverType('rgmii_phy[x].rxd3',   bus_phy, 'output', ['rgmii_mac[x].rxd3'], 1, False),

    DriverType('rgmii_phy[x].intn',  bus_phy, 'output', ['rgmii_mac[x].intn'], 1, True),
    DriverType('rgmii_mac[x].intn',  bus_mac, 'input',  ['rgmii_phy[x].intn'], 1, True),
    DriverType('rgmii_mac[x].rstn',  bus_mac, 'output', ['rgmii_phy[x].rstn'], 1, True),
    DriverType('rgmii_phy[x].rstn',  bus_phy, 'input',  ['rgmii_mac[x].rstn'], 1, True),

    DriverType('rgmii_mac[x].txc',    bus_mac, 'output', ['rgmii_phy[x].txc'], 1, False),
    DriverType('rgmii_mac[x].tx_ctl', bus_mac, 'output', ['rgmii_phy[x].tx_ctl'], 1, False),
    DriverType('rgmii_mac[x].txd0',   bus_mac, 'output', ['rgmii_phy[x].txd0'], 1, False),
    DriverType('rgmii_mac[x].txd1',   bus_mac, 'output', ['rgmii_phy[x].txd1'], 1, False),
    DriverType('rgmii_mac[x].txd2',   bus_mac, 'output', ['rgmii_phy[x].txd2'], 1, False),
    DriverType('rgmii_mac[x].txd3',   bus_mac, 'output', ['rgmii_phy[x].txd3'], 1, False),
    DriverType('rgmii_mac[x].rxc',    bus_mac, 'input',  ['rgmii_phy[x].rxc'], 1, False),
    DriverType('rgmii_mac[x].rx_ctl', bus_mac, 'input',  ['rgmii_phy[x].rx_ctl'], 1, False),
    DriverType('rgmii_mac[x].rxd0',   bus_mac, 'input',  ['rgmii_phy[x].rxd0'], 1, False),
    DriverType('rgmii_mac[x].rxd1',   bus_mac, 'input',  ['rgmii_phy[x].rxd1'], 1, False),
    DriverType('rgmii_mac[x].rxd2',   bus_mac, 'input',  ['rgmii_phy[x].rxd2'], 1, False),
    DriverType('rgmii_mac[x].rxd3',   bus_mac, 'input',  ['rgmii_phy[x].rxd3'], 1, False),

]

bus_mdio = [
    DriverType('mdio_slave[x].mdc',       bus_phy, 'input',         ['mdio_master[x].mdc'],  1, False),
    DriverType('mdio_slave[x].mdio',      bus_phy, 'bidirectional', ['mdio_master[x].mdio'], 1, False),
    DriverType('mdio_master[x].mdio',     bus_mac, 'bidirectional', ['mdio_slave[x].mdio'], 32, False),
    DriverType('mdio_master[x].mdc',      bus_mac, 'output',        ['mdio_slave[x].mdc'],  32, False),
]

bus_mdi1g = [
    DriverType('mdi1g_phy[x].dp0', bus_phy, 'bidirectional', ['mdi1g_conn[x].dp0'], 1, False),
    DriverType('mdi1g_phy[x].dm0', bus_phy, 'bidirectional', ['mdi1g_conn[x].dm0'], 1, False),
    DriverType('mdi1g_phy[x].dp1', bus_phy, 'bidirectional', ['mdi1g_conn[x].dp1'], 1, False),
    DriverType('mdi1g_phy[x].dm1', bus_phy, 'bidirectional', ['mdi1g_conn[x].dm1'], 1, False),
    DriverType('mdi1g_phy[x].dp2', bus_phy, 'bidirectional', ['mdi1g_conn[x].dp2'], 1, False),
    DriverType('mdi1g_phy[x].dm2', bus_phy, 'bidirectional', ['mdi1g_conn[x].dm2'], 1, False),
    DriverType('mdi1g_phy[x].dp3', bus_phy, 'bidirectional', ['mdi1g_conn[x].dp3'], 1, False),
    DriverType('mdi1g_phy[x].dm3', bus_phy, 'bidirectional', ['mdi1g_conn[x].dm3'], 1, False),

    DriverType('mdi1g_conn[x].dp0', bus_conn, 'bidirectional', ['mdi1g_phy[x].dp0'], 1, False),
    DriverType('mdi1g_conn[x].dm0', bus_conn, 'bidirectional', ['mdi1g_phy[x].dm0'], 1, False),
    DriverType('mdi1g_conn[x].dp1', bus_conn, 'bidirectional', ['mdi1g_phy[x].dp1'], 1, False),
    DriverType('mdi1g_conn[x].dm1', bus_conn, 'bidirectional', ['mdi1g_phy[x].dm1'], 1, False),
    DriverType('mdi1g_conn[x].dp2', bus_conn, 'bidirectional', ['mdi1g_phy[x].dp2'], 1, False),
    DriverType('mdi1g_conn[x].dm2', bus_conn, 'bidirectional', ['mdi1g_phy[x].dm2'], 1, False),
    DriverType('mdi1g_conn[x].dp3', bus_conn, 'bidirectional', ['mdi1g_phy[x].dp3'], 1, False),
    DriverType('mdi1g_conn[x].dm3', bus_conn, 'bidirectional', ['mdi1g_phy[x].dm3'], 1, False),
]

bus_mdi100m = [
    DriverType('mdi100m.phy[x]_rxp', bus_phy, 'bidirectional', ['mdi100m_conn[x].rxp'], 1, False),
    DriverType('mdi100m.phy[x]_rxm', bus_phy, 'bidirectional', ['mdi100m_conn[x].rxm'], 1, False),
    DriverType('mdi100m.phy[x]_txp', bus_phy, 'bidirectional', ['mdi100m_conn[x].txp'], 1, False),
    DriverType('mdi100m.phy[x]_txm', bus_phy, 'bidirectional', ['mdi100m_conn[x].txm'], 1, False),

    DriverType('mdi100m.conn[x]_rxp', bus_conn, 'bidirectional', ['mdi100m_phy[x].rxp'], 1, False),
    DriverType('mdi100m.conn[x]_rxm', bus_conn, 'bidirectional', ['mdi100m_phy[x].rxm'], 1, False),
    DriverType('mdi100m.conn[x]_txp', bus_conn, 'bidirectional', ['mdi100m_phy[x].txp'], 1, False),
    DriverType('mdi100m.conn[x]_txm', bus_conn, 'bidirectional', ['mdi100m_phy[x].txm'], 1, False),

]

bus_usbc = [

    DriverType('usbc_conn[x].txp',  bus_conn,   'bidirectional', ['usbc_master[x].txp'], 2, False),
    DriverType('usbc_conn[x].txm',  bus_conn,   'bidirectional', ['usbc_master[x].txm'], 2, False),
    DriverType('usbc_conn[x].vbus', bus_conn,   'bidirectional', ['usbc_master[x].vbus'], 2, False),
    DriverType('usbc_conn[x].cc',   bus_conn,   'bidirectional', ['usbc_master[x].cc'], 2, False),
    DriverType('usbc_conn[x].dp',   bus_conn,   'bidirectional', ['usbc_master[x].dp'], 2, False),
    DriverType('usbc_conn[x].dm',   bus_conn,   'bidirectional', ['usbc_master[x].dm'], 2, False),
    DriverType('usbc_conn[x].sbu',  bus_conn,   'bidirectional', ['usbc_master[x].sbu'], 2, False),
    DriverType('usbc_conn[x].vbus', bus_conn,   'bidirectional', ['usbc_master[x].vbus'], 2, False),
    DriverType('usbc_conn[x].rxm',  bus_conn,   'bidirectional', ['usbc_master[x].rxm'], 2, False),
    DriverType('usbc_conn[x].rxp',  bus_conn,   'bidirectional', ['usbc_master[x].rxp'], 2, False),

    DriverType('usbc_master[x].txp',  bus_master,   'bidirectional', ['usbc_conn[x].txp'],  2, False),
    DriverType('usbc_master[x].txm',  bus_master,   'bidirectional', ['usbc_conn[x].txm'],  2, False),
    DriverType('usbc_master[x].vbus', bus_master,   'bidirectional', ['usbc_conn[x].vbus'], 2, False),
    DriverType('usbc_master[x].cc',   bus_master,   'bidirectional', ['usbc_conn[x].cc'],  2, False),
    DriverType('usbc_master[x].dp',   bus_master,   'bidirectional', ['usbc_conn[x].dp'],  2, False),
    DriverType('usbc_master[x].dm',   bus_master,   'bidirectional', ['usbc_conn[x].dm'],  2, False),
    DriverType('usbc_master[x].sbu',  bus_master,   'bidirectional', ['usbc_conn[x].sbux'], 2, False),
    DriverType('usbc_master[x].vbus', bus_master,   'bidirectional', ['usbc_conn[x].vbus'], 2, False),
    DriverType('usbc_master[x].rxm',  bus_master,   'bidirectional', ['usbc_conn[x].rxm'],  2, False),
    DriverType('usbc_master[x].rxp',  bus_master,   'bidirectional', ['usbc_conn[x].rxp'],  2, False),


]


bus_lvds = [

    DriverType('lvds_rx[x].dpx_clkp', bus_slave, 'input', ['lvds_tx[x].dn0'], 1, False),
    DriverType('lvds_rx[x].dnx_clkn', bus_slave, 'input', ['lvds_tx[x].dn0'], 1, False),
    DriverType('lvds_rx[x].clkp', bus_slave, 'input', ['lvds_tx[x].dn0'], 1, False),
    DriverType('lvds_rx[x].clkn', bus_slave, 'input', ['lvds_tx[x].dp0'], 1, False),

    DriverType('lvds_rx[x].dn0', bus_slave, 'input', ['lvds_tx[x].dn0'], 1, False),
    DriverType('lvds_rx[x].dn1', bus_slave, 'input', ['lvds_tx[x].dn1'], 1, False),
    DriverType('lvds_rx[x].dn2', bus_slave, 'input', ['lvds_tx[x].dn2'], 1, False),
    DriverType('lvds_rx[x].dn3', bus_slave, 'input', ['lvds_tx[x].dn3'], 1, False),
    DriverType('lvds_rx[x].dn4', bus_slave, 'input', ['lvds_tx[x].dn4'], 1, False),
    DriverType('lvds_rx[x].dn5', bus_slave, 'input', ['lvds_tx[x].dn5'], 1, False),
    DriverType('lvds_rx[x].dn6', bus_slave, 'input', ['lvds_tx[x].dn6'], 1, False),
    DriverType('lvds_rx[x].dn7', bus_slave, 'input', ['lvds_tx[x].dn7'], 1, False),
    DriverType('lvds_rx[x].dn8', bus_slave, 'input', ['lvds_tx[x].dn8'], 1, False),
    DriverType('lvds_rx[x].dn9', bus_slave, 'input', ['lvds_tx[x].dn9'], 1, False),

    DriverType('lvds_rx[x].dp0', bus_slave, 'input', ['lvds_tx[x].dp0'], 1, False),
    DriverType('lvds_rx[x].dp1', bus_slave, 'input', ['lvds_tx[x].dp1'], 1, False),
    DriverType('lvds_rx[x].dp2', bus_slave, 'input', ['lvds_tx[x].dp2'], 1, False),
    DriverType('lvds_rx[x].dp3', bus_slave, 'input', ['lvds_tx[x].dp3'], 1, False),
    DriverType('lvds_rx[x].dp4', bus_slave, 'input', ['lvds_tx[x].dp4'], 1, False),
    DriverType('lvds_rx[x].dp5', bus_slave, 'input', ['lvds_tx[x].dp5'], 1, False),
    DriverType('lvds_rx[x].dp6', bus_slave, 'input', ['lvds_tx[x].dp6'], 1, False),
    DriverType('lvds_rx[x].dp7', bus_slave, 'input', ['lvds_tx[x].dp7'], 1, False),
    DriverType('lvds_rx[x].dp8', bus_slave, 'input', ['lvds_tx[x].dp8'], 1, False),
    DriverType('lvds_rx[x].dp9', bus_slave, 'input', ['lvds_tx[x].dp9'], 1, False),

    DriverType('lvds_tx[x].dn0', bus_master, 'output', ['lvds_rx[x].dn0'], 1, False),
    DriverType('lvds_tx[x].dn1', bus_master, 'output', ['lvds_rx[x].dn1'], 1, False),
    DriverType('lvds_tx[x].dn2', bus_master, 'output', ['lvds_rx[x].dn2'], 1, False),
    DriverType('lvds_tx[x].dn3', bus_master, 'output', ['lvds_rx[x].dn3'], 1, False),
    DriverType('lvds_tx[x].dn4', bus_master, 'output', ['lvds_rx[x].dn4'], 1, False),
    DriverType('lvds_tx[x].dn5', bus_master, 'output', ['lvds_rx[x].dn5'], 1, False),
    DriverType('lvds_tx[x].dn6', bus_master, 'output', ['lvds_rx[x].dn6'], 1, False),
    DriverType('lvds_tx[x].dn7', bus_master, 'output', ['lvds_rx[x].dn7'], 1, False),
    DriverType('lvds_tx[x].dn8', bus_master, 'output', ['lvds_rx[x].dn8'], 1, False),
    DriverType('lvds_tx[x].dn9', bus_master, 'output', ['lvds_rx[x].dn9'], 1, False),

    DriverType('lvds_tx[x].dp0', bus_slave, 'output', ['lvds_rx[x].dp0'], 1, False),
    DriverType('lvds_tx[x].dp1', bus_slave, 'output', ['lvds_rx[x].dp1'], 1, False),
    DriverType('lvds_tx[x].dp2', bus_slave, 'output', ['lvds_rx[x].dp2'], 1, False),
    DriverType('lvds_tx[x].dp3', bus_slave, 'output', ['lvds_rx[x].dp3'], 1, False),
    DriverType('lvds_tx[x].dp4', bus_slave, 'output', ['lvds_rx[x].dp4'], 1, False),
    DriverType('lvds_tx[x].dp5', bus_slave, 'output', ['lvds_rx[x].dp5'], 1, False),
    DriverType('lvds_tx[x].dp6', bus_slave, 'output', ['lvds_rx[x].dp6'], 1, False),
    DriverType('lvds_tx[x].dp7', bus_slave, 'output', ['lvds_rx[x].dp7'], 1, False),
    DriverType('lvds_tx[x].dp8', bus_slave, 'output', ['lvds_rx[x].dp8'], 1, False),
    DriverType('lvds_tx[x].dp9', bus_slave, 'output', ['lvds_rx[x].dp9'], 1, False),
]

bus_mipi = [
    DriverType('mipi_tx[x].dp0', bus_master, 'output', ['mipi_rx[x].dp0'], 1, False),
    DriverType('mipi_tx[x].dp1', bus_master, 'output', ['mipi_rx[x].dp1'], 1, False),
    DriverType('mipi_tx[x].dp2', bus_master, 'output', ['mipi_rx[x].dp2'], 1, False),
    DriverType('mipi_tx[x].dp3', bus_master, 'output', ['mipi_rx[x].dp3'], 1, False),
    DriverType('mipi_tx[x].dp4', bus_master, 'output', ['mipi_rx[x].dp4'], 1, False),

    DriverType('mipi_tx[x].dn0', bus_master, 'output', ['mipi_rx[x].dn0'], 1, False),
    DriverType('mipi_tx[x].dn1', bus_master, 'output', ['mipi_rx[x].dn1'], 1, False),
    DriverType('mipi_tx[x].dn2', bus_master, 'output', ['mipi_rx[x].dn2'], 1, False),
    DriverType('mipi_tx[x].dn3', bus_master, 'output', ['mipi_rx[x].dn3'], 1, False),
    DriverType('mipi_tx[x].dn4', bus_master, 'output', ['mipi_rx[x].dn4'], 1, False),

    DriverType('mipi_rx[x].dp0', bus_slave, 'output', ['mipi_tx[x].dp0'], 1, False),
    DriverType('mipi_rx[x].dp1', bus_slave, 'output', ['mipi_tx[x].dp1'], 1, False),
    DriverType('mipi_rx[x].dp2', bus_slave, 'output', ['mipi_tx[x].dp2'], 1, False),
    DriverType('mipi_rx[x].dp3', bus_slave, 'output', ['mipi_tx[x].dp3'], 1, False),
    DriverType('mipi_rx[x].dp4', bus_slave, 'output', ['mipi_tx[x].dp4'], 1, False),

    DriverType('mipi_rx[x].dn0', bus_slave, 'output', ['mipi_tx[x].dn0'], 1, False),
    DriverType('mipi_rx[x].dn1', bus_slave, 'output', ['mipi_tx[x].dn1'], 1, False),
    DriverType('mipi_rx[x].dn2', bus_slave, 'output', ['mipi_tx[x].dn2'], 1, False),
    DriverType('mipi_rx[x].dn3', bus_slave, 'output', ['mipi_tx[x].dn3'], 1, False),
    DriverType('mipi_rx[x].dn4', bus_slave, 'output', ['mipi_tx[x].dn4'], 1, False),

]

bus_system = [
    DriverType('system_master.rstn',    bus_master,   'output',    ['system_slave.rstn'], 1, False),
    DriverType('system_master.en',      bus_master,   'output',    ['system_slave.en'], 1, False),
    DriverType('system_master.gnd',     bus_powerout, 'power_out', ['system_slave.gnd'], 1, False),
    DriverType('system_master.gnd1',    bus_powerout, 'power_out', ['system_slave.gnd1'], 1, False),
    DriverType('system_master.gnd2',    bus_powerout, 'power_out', ['system_slave.gnd2'], 1, False),

    DriverType('system_master.vcc_id0',  bus_powerout, 'power_out', ['system_slave.vcc_id0'], 1, False),
    DriverType('system_master.vcc_id1',  bus_powerout, 'power_out', ['system_slave.vcc_id1'], 1, False),
    DriverType('system_master.vcc_id2',  bus_powerout, 'power_out', ['system_slave.vcc_id2'], 1, False),
    DriverType('system_master.vcc_id3',  bus_powerout, 'power_out', ['system_slave.vcc_id3'], 1, False),
    DriverType('system_master.vcc_id4',  bus_powerout, 'power_out', ['system_slave.vcc_id4'], 1, False),

    DriverType('system_master.vcc1v8',  bus_powerout, 'power_out', ['system_slave.vcc1v8'], 1, False),
    DriverType('system_master.vcc2v5',  bus_powerout, 'power_out', ['system_slave.vcc2v5'], 1, False),
    DriverType('system_master.vcc3v3',  bus_powerout, 'power_out', ['system_slave.vcc3v3'], 1, False),
    DriverType('system_master.vcc5v0',  bus_powerout, 'power_out', ['system_slave.vcc5v0'], 1, False),
    DriverType('system_master.vcc12v0', bus_powerout, 'power_out', ['system_slave.vcc12v0'], 1, False),

    DriverType('system_slave.rstn',    bus_slave,   'input',    ['system_master.rstn'], 1, False),
    DriverType('system_slave.en',      bus_slave,   'input',    ['system_master.en'], 1, False),
    DriverType('system_slave.gnd',     bus_powerin, 'power_in', ['system_master.gnd'], 1, False),
    DriverType('system_slave.gnd1',    bus_powerin, 'power_in', ['system_master.gnd1'], 1, False),
    DriverType('system_slave.gnd2',    bus_powerin, 'power_in', ['system_master.gnd2'], 1, False),

    DriverType('system_slave.vcc_id0',  bus_powerin, 'power_in', ['system_master.vcc_id0'], 1, False),
    DriverType('system_slave.vcc_id1',  bus_powerin, 'power_in', ['system_master.vcc_id1'], 1, False),
    DriverType('system_slave.vcc_id2',  bus_powerin, 'power_in', ['system_master.vcc_id2'], 1, False),
    DriverType('system_slave.vcc_id3',  bus_powerin, 'power_in', ['system_master.vcc_id3'], 1, False),
    DriverType('system_slave.vcc_id4',  bus_powerin, 'power_in', ['system_master.vcc_id4'], 1, False),

    DriverType('system_slave.vcc1v8',  bus_powerin, 'power_in', ['system_master.vcc1v8'], 1, False),
    DriverType('system_slave.vcc2v5',  bus_powerin, 'power_in', ['system_master.vcc2v5'], 1, False),
    DriverType('system_slave.vcc3v3',  bus_powerin, 'power_in', ['system_master.vcc3v3'], 1, False),
    DriverType('system_slave.vcc5v0',  bus_powerin, 'power_in', ['system_master.vcc5v0'], 1, False),
    DriverType('system_slave.vcc12v0', bus_powerin, 'power_in', ['system_master.vcc12v0'], 1, False),

]

# bus_mii = [
#     DriverType('mii_phy[x]_rxd0',   bus_phy, 'output', ['mii_mac[x]_rxd0'], 1, False),
#     DriverType('mii_phy[x]_rxd1',   bus_phy, 'output', ['mii_mac[x]_rxd1'], 1, False),
#     DriverType('mii_phy[x]_rxd2',   bus_phy, 'output', ['mii_mac[x]_rxd2'], 1, False),
#     DriverType('mii_phy[x]_rxd3',   bus_phy, 'output', ['mii_mac[x]_rxd3'], 1, False),
#     DriverType('mii_phy[x]_rx_dv',  bus_phy, 'output', ['mii_mac[x]_rx_dv'], 1, False),
#     DriverType('mii_phy[x]_rx_er',  bus_phy, 'output', ['mii_mac[x]_rx_er'], 1, False),
#     DriverType('mii_phy[x]_crs',    bus_phy, 'output', ['mii_mac[x]_crs'], 1, False),
#     DriverType('mii_phy[x]_col',    bus_phy, 'output', ['mii_mac[x]_col'], 1, False),
#     DriverType('mii_phy[x]_rx_clk', bus_phy, 'output', ['mii_mac[x]_rx_clk'], 1, False),
#     DriverType('mii_phy[x]_tx_clk', bus_phy, 'output', ['mii_mac[x]_tx_clk'], 1, False), # Both clocks in same direction?!

#     DriverType('mii_phy[x]_txd0',  bus_phy, 'input', ['mii_mac[x]_txd0'], 1, False),
#     DriverType('mii_phy[x]_txd1',  bus_phy, 'input', ['mii_mac[x]_txd1'], 1, False),
#     DriverType('mii_phy[x]_txd2',  bus_phy, 'input', ['mii_mac[x]_txd2'], 1, False),
#     DriverType('mii_phy[x]_txd3',  bus_phy, 'input', ['mii_mac[x]_txd3'], 1, False),
#     DriverType('mii_phy[x]_tx_en', bus_phy, 'input', ['mii_mac[x]_tx_en'], 1, False),
#     DriverType('mii_phy[x]_tx_er', bus_phy, 'input', ['mii_mac[x]_tx_er'], 1, True),
# ]

bus_rmii = [
    DriverType('rmii_phy[x].rxd0',      bus_phy, 'output', ['rmii_mac[x].rxd0'], 1, False),
    DriverType('rmii_phy[x].rxd1',      bus_phy, 'output', ['rmii_mac[x].rxd1'], 1, False),
    DriverType('rmii_phy[x].rx_er',     bus_phy, 'output', ['rmii_mac[x].rx_er'], 1, False),
    DriverType('rmii_phy[x].crs_rx_dv', bus_phy, 'output', ['rmii_mac[x].crs'], 1, False),
    DriverType('rmii_phy[x].rx_clk',    bus_phy, 'output', ['rmii_mac[x].rx_clk'], 1, True),
    DriverType('rmii_phy[x].intn',      bus_phy, 'output', ['rmii_mac[x].intn'], 1, True),

    DriverType('rmii_phy[x].txd0',  bus_phy, 'input', ['rmii_mac[x].txd0'], 1, False),
    DriverType('rmii_phy[x].txd1',  bus_phy, 'input', ['rmii_mac[x].txd1'], 1, False),
    DriverType('rmii_phy[x].tx_en', bus_phy, 'input', ['rmii_mac[x].tx_en'], 1, False),

    DriverType('rmii_mac[x].rxd0',      bus_mac, 'input', ['rmii_phy[x].rxd0'], 1, False),
    DriverType('rmii_mac[x].rxd1',      bus_mac, 'input', ['rmii_phy[x].rxd1'], 1, False),
    DriverType('rmii_mac[x].rx_er',     bus_mac, 'input', ['rmii_phy[x].rx_er'], 1, False),
    DriverType('rmii_mac[x].crs_rx_dv', bus_mac, 'input', ['rmii_phy[x].crs'], 1, False),
    DriverType('rmii_mac[x].rx_clk',    bus_mac, 'input', ['rmii_phy[x].rx_clk'], 1, True),
    DriverType('rmii_mac[x].intn',      bus_mac, 'input', ['rmii_phy[x].intn'], 1, True),

    DriverType('rmii_mac[x].txd0',  bus_mac, 'output', ['rmii_phy[x].txd0'], 1, False),
    DriverType('rmii_mac[x].txd1',  bus_mac, 'output', ['rmii_phy[x].txd1'], 1, False),
    DriverType('rmii_mac[x].tx_en', bus_mac, 'output', ['rmii_phy[x].tx_en'], 1, False),

    DriverType('rmii_phy[x].rstn', bus_phy, 'input', ['rmii_mac[x]_rstn'], 1, True),
    DriverType('rmii_mac[x].rstn', bus_mac, 'input', ['rmii_phy[x]_rstn'], 1, True),

]

bus_gpio = [
    DriverType('gpio[x].dio0', bus_gpio, 'bidirectional', ['gpio[x].dio0'], 1, True),
    DriverType('gpio[x].dio1', bus_gpio, 'bidirectional', ['gpio[x].dio1'], 1, True),
    DriverType('gpio[x].dio2', bus_gpio, 'bidirectional', ['gpio[x].dio2'], 1, True),
    DriverType('gpio[x].dio3', bus_gpio, 'bidirectional', ['gpio[x].dio3'], 1, True),
    DriverType('gpio[x].dio4', bus_gpio, 'bidirectional', ['gpio[x].dio4'], 1, True),
    DriverType('gpio[x].dio5', bus_gpio, 'bidirectional', ['gpio[x].dio5'], 1, True),
    DriverType('gpio[x].dio6', bus_gpio, 'bidirectional', ['gpio[x].dio6'], 1, True),
    DriverType('gpio[x].dio7', bus_gpio, 'bidirectional', ['gpio[x].dio7'], 1, True),

    DriverType('gpio[x].do0', bus_gpio, 'output', ['gpio[x].di0'], 1, True),
    DriverType('gpio[x].do1', bus_gpio, 'output', ['gpio[x].di1'], 1, True),
    DriverType('gpio[x].do2', bus_gpio, 'output', ['gpio[x].di2'], 1, True),
    DriverType('gpio[x].do3', bus_gpio, 'output', ['gpio[x].di3'], 1, True),
    DriverType('gpio[x].do4', bus_gpio, 'output', ['gpio[x].di4'], 1, True),
    DriverType('gpio[x].do5', bus_gpio, 'output', ['gpio[x].di5'], 1, True),
    DriverType('gpio[x].do6', bus_gpio, 'output', ['gpio[x].di6'], 1, True),
    DriverType('gpio[x].do7', bus_gpio, 'output', ['gpio[x].di7'], 1, True),

    DriverType('gpio[x].di0', bus_gpio, 'input', ['gpio[x].do0'], 1, True),
    DriverType('gpio[x].di1', bus_gpio, 'input', ['gpio[x].do1'], 1, True),
    DriverType('gpio[x].di2', bus_gpio, 'input', ['gpio[x].do2'], 1, True),
    DriverType('gpio[x].di3', bus_gpio, 'input', ['gpio[x].do3'], 1, True),
    DriverType('gpio[x].di4', bus_gpio, 'input', ['gpio[x].do4'], 1, True),
    DriverType('gpio[x].di5', bus_gpio, 'input', ['gpio[x].do5'], 1, True),
    DriverType('gpio[x].di6', bus_gpio, 'input', ['gpio[x].do6'], 1, True),
    DriverType('gpio[x].di7', bus_gpio, 'input', ['gpio[x].do7'], 1, True),

]

bus_adc = [
    DriverType('adc_master[x].a0', bus_master, 'input', ['adc_slave[x].a0'], 1, True),
    DriverType('adc_master[x].a1', bus_master, 'input', ['adc_slave[x].a1'], 1, True),
    DriverType('adc_master[x].a2', bus_master, 'input', ['adc_slave[x].a2'], 1, True),
    DriverType('adc_master[x].a3', bus_master, 'input', ['adc_slave[x].a3'], 1, True),
    DriverType('adc_master[x].a4', bus_master, 'input', ['adc_slave[x].a4'], 1, True),
    DriverType('adc_master[x].a5', bus_master, 'input', ['adc_slave[x].a5'], 1, True),
    DriverType('adc_master[x].a6', bus_master, 'input', ['adc_slave[x].a6'], 1, True),
    DriverType('adc_master[x].a7', bus_master, 'input', ['adc_slave[x].a7'], 1, True),

    DriverType('adc_slave[x].a0', bus_slave, 'output', ['adc_master[x].a0'], 1, True),
    DriverType('adc_slave[x].a1', bus_slave, 'output', ['adc_master[x].a1'], 1, True),
    DriverType('adc_slave[x].a2', bus_slave, 'output', ['adc_master[x].a2'], 1, True),
    DriverType('adc_slave[x].a3', bus_slave, 'output', ['adc_master[x].a3'], 1, True),
    DriverType('adc_slave[x].a4', bus_slave, 'output', ['adc_master[x].a4'], 1, True),
    DriverType('adc_slave[x].a5', bus_slave, 'output', ['adc_master[x].a5'], 1, True),
    DriverType('adc_slave[x].a6', bus_slave, 'output', ['adc_master[x].a6'], 1, True),
    DriverType('adc_slave[x].a7', bus_slave, 'output', ['adc_master[x].a7'], 1, True),
]


bus_list = [
    bus_qspi,
    bus_spi,
    bus_jtag,
    bus_usart,
    bus_i2c,
    bus_serialwire,
    bus_mdi1g,
    bus_rmii,
    bus_mdio,
    bus_rgmii,
    bus_mdi100m,
    bus_octaspi,
    bus_usbc,
    bus_adapter40p,
    bus_lvds,
    bus_mipi,
    bus_gpio,
    bus_adc,
    bus_system,
    # bus_rj45_conn,
]

bus_pin_drivers = {}
for bus in bus_list:
    for pin in bus:
        bus_pin_drivers[re.sub(r'\[x\]', '', pin.name)] = pin.kicad_driver