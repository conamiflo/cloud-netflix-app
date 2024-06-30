import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MovieReviewDialogComponent } from './movie-review-dialog.component';

describe('MovieReviewDialogComponent', () => {
  let component: MovieReviewDialogComponent;
  let fixture: ComponentFixture<MovieReviewDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MovieReviewDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MovieReviewDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
