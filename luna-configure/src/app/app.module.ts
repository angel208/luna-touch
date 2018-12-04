import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { HomeComponent } from './home/home.component';
import { TouchConfigComponent } from './touch-config/touch-config.component';
import { TtsConfigComponent } from './tts-config/tts-config.component';
import { TelegramConfigComponent } from './telegram-config/telegram-config.component';
import { StorageConfigComponent } from './storage-config/storage-config.component';

@NgModule({
  declarations: [
    AppComponent,
    SidebarComponent,
    HomeComponent,
    TouchConfigComponent,
    TtsConfigComponent,
    TelegramConfigComponent,
    StorageConfigComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent, SidebarComponent]
})
export class AppModule { }
