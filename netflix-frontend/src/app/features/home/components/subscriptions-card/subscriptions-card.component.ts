import {Component, Input} from '@angular/core';
import {IonIcon} from "@ionic/angular/standalone";
import {LowerCasePipe, NgForOf} from "@angular/common";
import {addIcons} from "ionicons";
import {send, star} from "ionicons/icons";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {SubscriptionService} from "../../../../core/services/subscription/subscription.service";

@Component({
  selector: 'app-subscriptions-card',
  standalone: true,
  imports: [
    IonIcon,
    NgForOf,
    LowerCasePipe
  ],
  templateUrl: './subscriptions-card.component.html',
  styleUrl: './subscriptions-card.component.css'
})
export class SubscriptionsCardComponent {
  @Input() subscription: any;
  constructor( private cognitoService: CognitoService,
               private subscriptionService: SubscriptionService) {
    addIcons({star,send});
  }

  unsubscribe() {
    this.subscriptionService.unsubscribe(this.subscription.username, this.subscription.subscription_id).subscribe(response => {
      alert(`Unsubscribed from ${this.subscription.type.toLowerCase()} ${this.subscription.value}`);
    }, error => {
      console.error('Error unsubscribing:', error);
      alert('Could not unsubscribe from subscription');
    });
  }

}
