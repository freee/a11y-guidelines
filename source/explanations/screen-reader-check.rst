.. _exp-screen-reader-check:

##############################################
スクリーン・リーダーを用いたチェックの実施方法
##############################################

ここでは、主要なスクリーン・リーダーを用いてチェックする場合に推奨される設定や最低限知っておくべき事項について説明します。

なお、freeeでは以下の方針でスクリーン・リーダーによるチェックを実施しています。

PC向けWeb
   *  Windows上のNVDAとGoogle Chromeで動作確認し、動作しない場合は当該チェックの結果をNGとする
   *  macOS VoiceOverによるチェックは、スタティックなコンテンツや既にNVDAでの動作確認が完了しているUIコンポーネントに限定し、その他のチェックはNVDAで実施する
モバイル・アプリケーション
   *  iOS VoiceOver、Android TalkBackそれぞれでで動作確認し、動作しない場合は当該チェックの結果をNGとする

.. toctree::
   :titlesonly:

   screen-reader-check-nvda
   screen-reader-check-macos-voiceover
   screen-reader-check-ios-voiceover
   screen-reader-check-android-talkback
