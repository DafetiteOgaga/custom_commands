import { Link, Stack, usePathname } from 'expo-router';
import { StyleSheet } from 'react-native';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { ScreenStyle } from '../myConfig/navigation';


export default function NotFoundScreen() {
  const pathname = usePathname();
  return (
    <>
      {/* hide the header in the Stack.Screen */}
      <Stack.Screen options={{ headerShown: false }} />
      <ThemedView style={[ScreenStyle.allScreenContainer, styles.container]}>
        <ThemedText type="title">This screen doesn't exist.</ThemedText>
        <Link href="/" style={styles.link}>
          <ThemedText type="link">Go to home screen!</ThemedText>
        </Link>
      </ThemedView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
});
