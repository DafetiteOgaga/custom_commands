import { Link, Stack } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import React from 'react';
import { ThemedText } from '../components/ThemedText';
import { ThemedView } from '../components/ThemedView';
import ScreenStyle from '@/hooks/ScreenStyle';

export default function TestScreen() {
  return (
    <>
      <Stack.Screen />
      <ThemedView style={[ScreenStyle.allScreenContainer, styles.container]}>
        <ThemedText type="title">This is a test screen.</ThemedText>
        <ThemedText type="link">Go nowhere!</ThemedText>
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
    // marginTop: 15,
    paddingVertical: 15,
  },
});
