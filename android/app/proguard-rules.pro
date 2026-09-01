# Capacitor-Plugins werden ueber Reflection geladen.
-keep class com.getcapacitor.** { *; }
-keep class com.capacitorjs.** { *; }
-keepclassmembers class * extends com.getcapacitor.Plugin { *; }
