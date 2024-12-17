/**
  ******************************************************************************
  * File Name          : app_touchgfx.c
  ******************************************************************************
  * This file was created by TouchGFX Generator 4.24.0. This file is only
  * generated once! Delete this file from your project and re-generate code
  * using STM32CubeMX or change this file manually to update it.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "app_touchgfx.h"
#include "stm32f7xx_hal.h" // HAL STM32

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private define ------------------------------------------------------------*/

/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void touchgfx_init(void);
void touchgfx_components_init(void);
void touchgfx_taskEntry(void);

/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/**
 * PreOS Initialization function
 */
void MX_TouchGFX_PreOSInit(void)
{
}

/**
 * Initialize TouchGFX application
 */
void MX_TouchGFX_Init(void)
{
    // Calling forward to touchgfx_init in C++ domain
    touchgfx_components_init();
    touchgfx_init();
}

/**
 * TouchGFX application entry function
 */
void MX_TouchGFX_Process(void)
{
    // Calling forward to touchgfx_taskEntry in C++ domain
    touchgfx_taskEntry();
}

/**
 * TouchGFX application thread
 */
// Déclaration de la fonction TouchGFX pour un fichier C
extern void touchgfx_taskEntry(void);

// Variable pour contrôler la mise en veille
volatile uint8_t goToSleep = 1;

void TouchGFX_Task(void *argument) {
    for (;;) {
        if (goToSleep) {
            // Suspendre l'exécution de TouchGFX et mettre en veille
            HAL_SuspendTick(); // Désactiver SysTick pour économiser l'énergie
            HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
            HAL_ResumeTick(); // Réactiver SysTick après le réveil

            goToSleep = 0; // Réinitialiser l'état après le réveil
        }

        // Appel normal de la boucle TouchGFX
        touchgfx_taskEntry();
    }
}

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
