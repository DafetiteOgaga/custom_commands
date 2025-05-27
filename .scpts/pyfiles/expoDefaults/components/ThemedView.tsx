import { View, type ViewProps } from 'react-native';

import { useThemeColor } from '@/hooks/useThemeColor';
import { useCurrColorMode } from '@/constants/Colors';

export type ThemedViewProps = ViewProps & {
  lightColor?: string;
  darkColor?: string;
};

export function ThemedView({ style, lightColor, darkColor, ...otherProps }: ThemedViewProps) {
  // const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, 'background');
  const backgroundColor = useThemeColor({ light: lightColor, dark: 'black' }, 'background');
  const deviceColorScheme = useCurrColorMode();

  // return <View style={[{ backgroundColor: deviceColorScheme.vvvdrkb }, style]} {...otherProps} />;
  return <View style={[{ backgroundColor }, style]} {...otherProps} />;
  // return <View style={[style]} {...otherProps} />;
}
