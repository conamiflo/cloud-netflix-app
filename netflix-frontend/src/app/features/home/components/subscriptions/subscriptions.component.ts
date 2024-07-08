import {Component, OnInit} from '@angular/core';
import {SubscriptionsCardComponent} from "../subscriptions-card/subscriptions-card.component";
import {MovieService} from "../../../../core/services/movie/movie.service";
import {SubscriptionService} from "../../../../core/services/subscription/subscription.service";
import {CognitoService} from "../../../../core/services/cognito/cognito.service";
import {Form, FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {MovieReviewComponent} from "../movies/movie-review/movie-review.component";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-subscriptions',
  standalone: true,
  imports: [
    SubscriptionsCardComponent,
    ReactiveFormsModule,
    MovieReviewComponent,
    NgForOf
  ],
  templateUrl: './subscriptions.component.html',
  styleUrl: './subscriptions.component.css'
})
export class SubscriptionsComponent implements OnInit{
  username: string | null = null;
  subscriptionsGenreForm: FormGroup;
  subscriptionsActorForm: FormGroup;
  subscriptionsDirectorForm: FormGroup;
  subscriptions: any[] = [];

  constructor(private fb: FormBuilder,
              private cognitoService: CognitoService,
              private subscriptionService: SubscriptionService) {
    this.loadUsername();
  }
  async loadUsername() {
    this.username = await this.cognitoService.getUsername();
    this.loadSubscriptions();
  }

  ngOnInit(): void {
    this.subscriptionsGenreForm = this.fb.group({
      genre: ['', [Validators.required, Validators.minLength(3)]],
    });
    this.subscriptionsActorForm = this.fb.group({
      actor: ['', [Validators.required, Validators.minLength(3)]],
    });
    this.subscriptionsDirectorForm = this.fb.group({
      director: ['', [Validators.required, Validators.minLength(3)]]
    });
  }

  async loadSubscriptions(): Promise<void> {
    if (this.username) {
      (await this.subscriptionService.getSubscriptions(this.username)).subscribe(
        (response) => {
          this.subscriptions = response.subscriptions;
        },
        (error) => {
          console.error('Error loading subscriptions:', error);
        }
      );
    } else {
      console.error('User is not logged in.');
    }
  }

  async subscribeToGenre() {
    if (this.subscriptionsGenreForm.valid) {
      if (this.username) {
        (await this.subscriptionService.subscribe(this.username, 'Genre', this.subscriptionsGenreForm.get('genre')?.value)).subscribe(response => {
          alert(`Subscribed to genre ${this.subscriptionsGenreForm.get('genre')?.value}`)
        }, error => {
          console.error(error);
          alert('You cannot subscribe to that genre');
        });
      }
    } else {
      alert('Invalid genre!')
    }
  }

  async subscribeToActor() {
    if (this.subscriptionsActorForm.valid) {
      if (this.username) {
        (await this.subscriptionService.subscribe(this.username, 'Actor', this.subscriptionsActorForm.get('actor')?.value)).subscribe(response => {
          alert(`Subscribed to actor ${this.subscriptionsActorForm.get('actor')?.value}`)
        }, error => {
          console.error(error);
          alert('You cannot subscribe to that actor');
        });
      } else {
        console.error('User is not logged in.');
      }
    } else {
      alert('Invalid actor!')
    }
  }

  async subscribeToDirector() {
    if (this.subscriptionsDirectorForm.valid) {
      if (this.username) {
        (await this.subscriptionService.subscribe(this.username, 'Director', this.subscriptionsDirectorForm.get('director')?.value)).subscribe(response => {
          alert(`Subscribed to director ${this.subscriptionsDirectorForm.get('director')?.value}`)
        }, error => {
          console.error(error);
          alert('You cannot subscribe to that director');
        });
      } else {
        console.error('User is not logged in.');
      }
    } else {
      alert('Invalid director!')
    }
  }

  handleUnsubscribed(subscriptionId: string) {
    this.subscriptions = this.subscriptions.filter(sub => sub.subscription_id !== subscriptionId);
  }

}
