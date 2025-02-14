import type { PropsWithChildren, ReactElement } from 'react';
import { StyleSheet } from 'react-native';
import Animated, {
  interpolate,
  useAnimatedRef,
  useAnimatedStyle,
  useScrollViewOffset,
  runOnJS,
} from 'react-native-reanimated';

import { ThemedView } from '@/components/ThemedView';
import { useBottomTabOverflow } from '@/components/ui/TabBarBackground';
import { useColorScheme } from '@/hooks/useColorScheme';

const HEADER_HEIGHT = 250;
const DEFAULT_CHILDREN_PADDING = 32;

type Props = PropsWithChildren<{
  headerImage: ReactElement;
  headerBackgroundColor: { dark: string; light: string };
  headerHeight?: number;
  childrenPadding?: number;
  onScrollOffsetChange?: any;
}>;

export default function ParallaxScrollView({
  children,
  headerImage,
  headerBackgroundColor,
  headerHeight = HEADER_HEIGHT,
  childrenPadding = DEFAULT_CHILDREN_PADDING,
  onScrollOffsetChange
}: Props) {
  const colorScheme = useColorScheme() ?? 'light';
  const scrollRef = useAnimatedRef<Animated.ScrollView>();
  const scrollOffset = useScrollViewOffset(scrollRef);
  const bottom = useBottomTabOverflow();
  const dynamicStyles = StyleSheet.create({
    height: {
      height: headerHeight,
    },
    childrenPadding: {
      padding: childrenPadding
    }
  });
  const headerAnimatedStyle = useAnimatedStyle(() => {
    const offset = scrollOffset.value;
    // console.log({offset});
    if (onScrollOffsetChange)
      runOnJS(onScrollOffsetChange)(offset);
    return {
      transform: [
        {
          translateY: interpolate(
            offset,
            [-headerHeight, 0, headerHeight],
            [-headerHeight / 2, 0, headerHeight * 0.75]
          ),
        },
        {
          scale: interpolate(offset, [-headerHeight, 0, headerHeight], [2, 1, 1]),
        },
      ],
    };
  });

  return (
    <ThemedView style={styles.container}>
      <Animated.ScrollView
        ref={scrollRef}
        scrollEventThrottle={16}
        scrollIndicatorInsets={{ bottom }}
        contentContainerStyle={{ paddingBottom: bottom }}>
        <Animated.View
          style={[
            styles.header, dynamicStyles.height,
            { backgroundColor: headerBackgroundColor[colorScheme] },
            headerAnimatedStyle,
          ]}>
          {headerImage}
        </Animated.View>
        <ThemedView style={[styles.content,dynamicStyles.childrenPadding]}>{children}</ThemedView>
      </Animated.ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
    overflow: 'hidden',
    borderRadius: 10,
  },
  content: {
    flex: 1,
    gap: 16,
    overflow: 'hidden',
  },
});
