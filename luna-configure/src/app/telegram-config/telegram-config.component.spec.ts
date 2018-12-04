import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TelegramConfigComponent } from './telegram-config.component';

describe('TelegramConfigComponent', () => {
  let component: TelegramConfigComponent;
  let fixture: ComponentFixture<TelegramConfigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TelegramConfigComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TelegramConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
