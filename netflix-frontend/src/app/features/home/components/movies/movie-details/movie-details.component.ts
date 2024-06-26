import { Component, OnInit } from '@angular/core';
import { addIcons} from 'ionicons';
import {IonIcon} from '@ionic/angular/standalone'
import { cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp ,calendarOutline,timeOutline} from 'ionicons/icons';

@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [IonIcon],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent{
  constructor() {
    addIcons({ cameraOutline, playCircle, shareSocial, play, downloadOutline, chevronUp,calendarOutline,timeOutline});
  }
}

