import { useColorScheme } from 'react-native';
/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

const tintColorLight = '#0a7ea4';
const tintColorDark = '#fff';

export const Colors = {
  light: {
    text: '#11181C',
    background: 'whitesmoke',
    tint: tintColorLight,
    icon: '#687076',
    tabIconDefault: '#687076',
    tabIconSelected: tintColorLight,
    smoke: '#e5e5e9',
  },
  dark: {
    text: '#ECEDEE',
    // background: '#0f324B',
    background: '#1C1C1C',
    // background: '#242f2f',
    tint: tintColorDark,
    icon: '#9BA1A6',
    tabIconDefault: '#9BA1A6',
    tabIconSelected: tintColorDark,
    smoke: '#whitesmoke',
  },
};

export const useCurrColorMode = () => {
  const colorScheme = useColorScheme(); // Detect system theme
  // console.log({colorScheme});
  return colorScheme === 'dark' ? Colors.dark : Colors.light;
};

export const useCurrColorModeTransparent = () => {
  const colorScheme = useColorScheme(); // Detect system theme
  // console.log({colorScheme});
  return colorScheme === 'dark' ? '#121a1d' : 'rgba(255, 255, 255, 0.8)'
  // return colorScheme === 'dark' ? '#291c1c' : '#ffffff'
};