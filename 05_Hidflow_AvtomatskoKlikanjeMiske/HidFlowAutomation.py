import pyautogui

#############FILL FORM FROM TRAINING#######################
# pyautogui.moveTo(123, 357, 1, pyautogui.easeInQuad)
# pyautogui.click()
# pyautogui.typewrite('avion')
# pyautogui.moveTo(153, 426, 1, pyautogui.easeInQuad)
# pyautogui.click()
# pyautogui.typewrite('leti leti leti')
# pyautogui.moveTo(242, 493, 1, pyautogui.easeInQuad)
# pyautogui.click()
# pyautogui.press('down')
# pyautogui.press('enter')
# pyautogui.moveTo(309, 602, 1, pyautogui.easeInQuad)
# pyautogui.click()
# pyautogui.moveTo(134, 711, 1, pyautogui.easeInQuad)
# pyautogui.click()
# pyautogui.typewrite('leti leti leti')

print(pyautogui.position())

for i in range(10):
    pyautogui.moveTo(882, 576, 1, pyautogui.easeInQuad)
    pyautogui.click()
    pyautogui.PAUSE = 10
