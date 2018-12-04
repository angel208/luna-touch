import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SidebarComponent } from './sidebar/sidebar.component';
import { HomeComponent } from './home/home.component';
import { TouchConfigComponent } from './touch-config/touch-config.component';
import { TelegramConfigComponent } from './telegram-config/telegram-config.component';
import { TtsConfigComponent } from './tts-config/tts-config.component';
import { StorageConfigComponent } from './storage-config/storage-config.component';

const routes: Routes = [
  
  { path: 'touch', component: TouchConfigComponent},
  { path: 'tts', component: TtsConfigComponent},
  { path: 'telegram', component: TelegramConfigComponent},
  { path: 'storage', component: StorageConfigComponent},
  { path: '', component: HomeComponent, pathMatch: 'full'},
  { path: '**', redirectTo:'/' , pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
