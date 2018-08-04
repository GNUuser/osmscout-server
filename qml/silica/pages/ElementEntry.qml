/*
 * Copyright (C) 2016-2018 Rinigus https://github.com/rinigus
 * 
 * This file is part of OSM Scout Server.
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import QtQuick 2.0
import Sailfish.Silica 1.0

Column {
    id: main

    property string key
    property string mainLabel
    property string secondaryLabel
    property bool hasUnits: false
    property double displayFactor: 1.0

    property alias value: textInput.text
    property alias validator: textInput.validator
    property alias inputMethodHints: textInput.inputMethodHints

    width: parent.width
    anchors.margins: Theme.horizontalPageMargin
    spacing: Theme.paddingSmall

    function apply()
    {
        if (textInput.acceptableInput)
        {
            var rep = value
            if (main.hasUnits)
                rep = parseFloat(value) / main.displayFactor

            settings.setValue(key, rep)
        }
    }

    TextField {
        id: textInput
        width: parent.width
        text: ""
        label: parent.mainLabel
        placeholderText: parent.mainLabel

        Component.onCompleted: {
            text = settings.valueString(main.key)
            main.hasUnits = settings.hasUnits(main.key)
            if (main.hasUnits)
            {
                main.displayFactor = settings.unitFactor();
                validator.decimals = settings.unitDisplayDecimals()

                var v = parseFloat(text) * main.displayFactor
                text = v.toFixed(settings.unitDisplayDecimals())

                label = label + ", " + settings.unitName(main.key)
            }
        }

        EnterKey.enabled: text.length > 0
        EnterKey.onClicked: {
            /// commented out since we apply settings separately
            // settings.setValue(parent.key, parent.value)
            focus = false
        }

//        onFocusChanged: {
//            if (!focus)
//            {
//                if (settings.valueString(parent.key) !== text)
//                {
//                    secLabel.text = "<b>Setting not applied.</b> " + parent.secondaryLabel
//                    secLabel.visible = true
//                }
//                else
//                {
//                    secLabel.text = parent.secondaryLabel
//                    secLabel.visible = (parent.secondaryLabel.length > 0)
//                }
//            }
//        }
    }

    Label {
        id: secLabel
        text: parent.secondaryLabel
        x: Theme.horizontalPageMargin
        width: parent.width-2*x
        wrapMode: Text.WordWrap
        font.pixelSize: Theme.fontSizeSmall
        color: Theme.highlightColor

        Component.onCompleted: { visible = (parent.secondaryLabel.length > 0) }
    }
}

