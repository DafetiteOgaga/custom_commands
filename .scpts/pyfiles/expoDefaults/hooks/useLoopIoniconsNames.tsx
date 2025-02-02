import { useState } from "react";
import { Ionicons } from '@expo/vector-icons';

type IconNameTYpe = keyof typeof Ionicons.glyphMap;

const useGetIconName = (): { iconName: IconNameTYpe; getNextName: () => void } => {
	const names = [
		"add",
		"add-circle",
		"alert",
		"alert-circle",
		"aperture",
		"apps",
		"archive",
		"arrow-back",
		"arrow-forward",
		"arrow-down",
		"arrow-up",
		"arrow-redo",
		"arrow-undo",
		"attach",
		"backspace",
		"bag",
		"bar-chart",
		"battery-charging",
		"battery-full",
		"battery-half",
		"beaker",
		"bed",
		"bookmark",
		"book",
		"briefcase",
		"build",
		"bulb",
		"calendar",
		"camera",
		"car",
		"cart",
		"chatbox",
		"chatbubble",
		"checkmark",
		"chevron-back",
		"chevron-forward",
		"chevron-down",
		"chevron-up",
		"clipboard",
		"close",
		"cloud",
		"cloud-download",
		"cloud-upload",
		"code",
		"color-filter",
		"color-palette",
		"compass",
		"copy",
		"create",
		"cube",
		"document",
		"download",
		"earth",
		"eye",
		"eye-off",
		"fast-food",
		"film",
		"filter",
		"flash",
		"flask",
		"folder",
		"game-controller",
		"globe",
		"grid",
		"hammer",
		"heart",
		"help",
		"home",
		"image",
		"information-circle",
		"key",
		"leaf",
		"library",
		"link",
		"list",
		"lock",
		"log-in",
		"log-out",
		"mail",
		"map",
		"medal",
		"megaphone",
		"menu",
		"mic",
		"moon",
		"notifications",
		"paper-plane",
		"pencil",
		"person",
		"phone",
		"pie-chart",
		"pin",
		"play",
		"power",
		"radio",
		"reader",
		"refresh",
		"reload",
		"rocket",
		"save",
		"search",
		"send",
		"settings",
		"share",
		"shield",
		"star",
		"stopwatch",
		"storefront",
		"sync",
		"time",
		"timer",
		"trash",
		"trending-up",
		"umbrella",
		"videocam",
		"volume-high",
		"wallet",
		"warning",
		"wifi"
	];
	const [currName, setCurrName] = useState<string>('home');
	const [nameList, setNameList] = useState<string[]>(names);
	const getNextName = (): void => {
		if (nameList.length === 0) {
			console.log("No more names left!");
			setCurrName("home");
			return;
		}
		setNameList((prevList) => {
			const updatedList = [...prevList];
			const name = updatedList.shift();
			setCurrName(name ?? "home");
			return updatedList;
		});
	};
	const iconName = currName as keyof typeof Ionicons.glyphMap
	// console.log('#####',{currName})
	return {iconName, getNextName};
}
export default useGetIconName;