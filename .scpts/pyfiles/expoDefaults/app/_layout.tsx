import { DarkTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';
// import { Text, View } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import 'react-native-reanimated';
import DrawerNavigator from '../navigations/drawerSetup';
import { useColorMode } from '@/constants/Colors';
import Toast, { BaseToast, ErrorToast } from 'react-native-toast-message';

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const deviceColorScheme = useColorMode();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return (
    // Wrap the app in the GestureHandlerRootView to enable gesture handling
    <>
      <GestureHandlerRootView style={{ flex: 1 }}>
        <ThemeProvider value={{
                    ...DarkTheme,
                    colors: {
                      ...DarkTheme.colors,
                      background: 'black',
                      // text: '#FF5733',
                    }}}>
          <DrawerNavigator // The DrawerNavigator component (wraps the entire app)
          />
        </ThemeProvider>
      </GestureHandlerRootView>
      <Toast
        config={toastConfig}
        position="top"
        visibilityTime={3000}
        topOffset={150}
        bottomOffset={40}
      />
    </>
  );
}

const toastStyles = {
  mainStyles: {
    zIndex: 500,
    borderLeftWidth: 20,
    backgroundColor: 'rgba(128, 128, 128, 0.7)',
    height: 30,
    paddingVertical: 5,
    paddingHorizontal: 5,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  text1Style: {
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
    color: '#ffffff',
  },
  text2Style: {
    fontSize: 14,
    textAlign: 'center',
    color: '#f1f1f1',
  }
}
const toastConfig = {
  success: (props: any) => (
    <BaseToast
      {...props}
      style={[toastStyles.mainStyles, {borderLeftColor: '#4CAF50',}]}
      text1Style={toastStyles.text1Style}
      text2Style={toastStyles.text2Style}
    />
  ),
  error: (props: any) => (
    <ErrorToast
      {...props}
      style={[toastStyles.mainStyles, {borderLeftColor: '#E74C3C',}]}
      text1Style={toastStyles.text1Style}
      text2Style={toastStyles.text2Style}
    />
  ),
  info: (props: any) => (
    <BaseToast
      {...props}
      style={[toastStyles.mainStyles, {borderLeftColor: '#3498db',}]}
      text1Style={toastStyles.text1Style}
      text2Style={toastStyles.text2Style}
    />
  ),
  warning: (props: any) => (
    <BaseToast
      {...props}
      style={[toastStyles.mainStyles, {borderLeftColor: '#f1c40f',}]}
      text1Style={toastStyles.text1Style}
      text2Style={toastStyles.text2Style}
    />
  ),
};


// Toast.show({
//   type: 'error', // 'success' | 'error' | 'info'
//   text1: 'Oops! Something went wrong',
//   text2: 'Please try again later',
//   position: 'bottom', // 'top' | 'bottom'
//   visibilityTime: 3000, // Hide after 3 seconds
// });
