#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "helpers.h"
#include "shared.h"
#include "max572x.h"

// SPI_POLARITY_LOW is a must
// if SPI_PHASE_1EDGE, DPHA = 0
// if SPI_PHASE_2EDGE, DPHA = 1

void print_3b(uint8_t buf[3])
{
  printf("0x%x 0x%x 0x%x\n", buf[0], buf[1], buf[2]);
}

void max572x_SW_RESET()
{
  uint8_t max572x_cmd_SW_RESET[3] = {0x35, 0x96, 0x30};
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, max572x_cmd_SW_RESET, 3, 100);
  spi_cs_high();
  // printf("max572x_SW_RESET\n");
}

/*
  dac_multi_sel: each bit selects a coresponding DAC
  power_mode: one of the max572x_POWER_XXX defines in the header file
*/
void max572x_POWER(uint8_t dac_multi_sel, uint8_t power_mode)
{
  uint8_t spi_sb[3] = {0x40, dac_multi_sel, power_mode};
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max572x_POWER: "); print_3b(spi_sb);
}

/*
  dac_multi_sel: each bit selects a coresponding DAC
  wdog: look at datasheet page 26 for details
  gate_en: 0 enable software gating, 1 disable
  ldac_en: 0 DAC latch enabled, 1 DAC latch transparent
  clear_en: 0 clear input and command works, 1 clear has no effect
*/
void max572x_CONFIG(uint8_t dac_multi_sel, uint8_t wdog, uint8_t gate_en, uint8_t ldac_en, uint8_t clear_en)
{
  uint8_t spi_sb[3] = {0x50, dac_multi_sel, 0};
  spi_sb[2] |= wdog;
  if(gate_en)
    spi_sb[2] |= max572x_CONFIG_GATE_EN;
  if(ldac_en)
    spi_sb[2] |= max572x_CONFIG_LDAC_EN;
  if(clear_en)
    spi_sb[2] |= max572x_CONFIG_CLR_EN;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max572x_CONFIG: "); print_3b(spi_sb);
}

/*
  wd_timeout: 12-bit timeout value in ms, max 4096ms
  wd_mask: when 1 timeout will not assert IRQ
  wd_safety: one of the max572x_WDOG_SAFETY_XXX defines in header file
*/
void max572x_WDOG(uint16_t wd_timeout, uint8_t wd_mask, uint8_t wd_safety)
{
  uint8_t spi_sb[3] = {0x10, 0, 0};
  wd_timeout &= 0xfff;
  spi_sb[1] |= wd_timeout >> 4;
  wd_timeout &= 0xf;
  spi_sb[2] |= (wd_timeout << 4);
  if(wd_mask)
    spi_sb[2] |= max572x_WDOG_WD_MASK;
  spi_sb[2] |= wd_safety;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max572x_WDOG: "); print_3b(spi_sb);
}

/*
  ref_power: 0 auto power off, 1 always on
  ref_mode: one of the max572x_REF_XXX defines in header file
*/
void max572x_REF(uint8_t ref_power, uint8_t ref_mode)
{
  uint8_t spi_sb[3] = {0x20, 0, 0};
  if(ref_power)
    spi_sb[0] |= max572x_REF_POWER;
  spi_sb[0] |= ref_mode;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max572x_REF: "); print_3b(spi_sb);
}

void max5723_CODEn(uint8_t dac_sel, uint8_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  spi_sb[1] = data;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5723_CODEn: "); print_3b(spi_sb);
}

void max5724_CODEn(uint8_t dac_sel, uint16_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  data &= 0x3ff;
  spi_sb[1] |= data >> 2;
  data &= 0x3;
  spi_sb[2] |= (data << 6);
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5724_CODEn: "); print_3b(spi_sb);
}

void max5725_CODEn(uint8_t dac_sel, uint16_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  data &= 0xfff;
  spi_sb[1] |= data >> 4;
  data &= 0xf;
  spi_sb[2] |= (data << 4);
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5725_CODEn: "); print_3b(spi_sb);
}

void max572x_LOADn(uint8_t dac_sel)
{
  uint8_t spi_sb[3] = {0x90, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max572x_LOADn: "); print_3b(spi_sb);
}

void test(void)
{
  max572x_SW_RESET();
  max572x_CONFIG(0x3, max572x_CONFIG_WDOG_DISABLE, 1, 1, 0);
  max572x_WDOG(0xff, 1, max572x_WDOG_SAFETY_LOW);
  max572x_REF(1, max572x_REF_2V5);
  max572x_POWER(0xff, max572x_POWER_HIZ);
  max572x_POWER(0x3, max572x_POWER_NORMAL);

  printf("run started\n");
  uint16_t count = 0;
  while(1)
  {
    max5724_CODEn(0, ~count);
    max5724_CODEn(1, count);
    count++;
  }
}
