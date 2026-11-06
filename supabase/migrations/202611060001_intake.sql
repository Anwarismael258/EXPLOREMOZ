begin;

-- A verified email account can send a support ticket without a KYC application.
create table public.exploremoz_support (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id),
  subject text not null check (char_length(btrim(subject)) between 4 and 150),
  message text not null check (char_length(btrim(message)) between 10 and 4000),
  status text not null default 'received' check (status in ('received','in_progress','closed')),
  created_at timestamptz not null default now()
);
create index on public.exploremoz_support (user_id, created_at desc);
alter table public.exploremoz_support enable row level security;
revoke all on public.exploremoz_support from public, anon, authenticated;
grant select on public.exploremoz_support to authenticated;
grant insert (subject, message) on public.exploremoz_support to authenticated;
create policy exploremoz_read_own_ticket on public.exploremoz_support
  for select to authenticated using (user_id = (select auth.uid()));
create policy exploremoz_send_own_ticket on public.exploremoz_support
  for insert to authenticated with check (user_id = (select auth.uid()));

create table public.exploremoz_partner_applications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id),
  partner_type text not null check (partner_type in (
    'accommodation','restaurant','operator','guide','transport','events','other'
  )),
  display_name text not null check (char_length(btrim(display_name)) between 2 and 150),
  status text not null default 'pending_documents' check (status in (
    'pending_documents','pending_review','correction_requested','approved','rejected'
  )),
  created_at timestamptz not null default now(),
  unique (user_id)
);
alter table public.exploremoz_partner_applications enable row level security;
revoke all on public.exploremoz_partner_applications from public, anon, authenticated;
grant select on public.exploremoz_partner_applications to authenticated;
grant insert (partner_type, display_name) on public.exploremoz_partner_applications to authenticated;
create policy exploremoz_read_own_application on public.exploremoz_partner_applications
  for select to authenticated using (user_id = (select auth.uid()));
create policy exploremoz_start_own_application on public.exploremoz_partner_applications
  for insert to authenticated with check (user_id = (select auth.uid()));

-- A worker can deliver these events after the Central's authenticated receiver is configured.
create schema if not exists exploremoz_internal;
revoke all on schema exploremoz_internal from public, anon, authenticated;
create table exploremoz_internal.outbox (
  id uuid primary key default gen_random_uuid(),
  event_type text not null,
  resource_id uuid not null,
  created_at timestamptz not null default now(),
  delivered_at timestamptz,
  unique (event_type, resource_id)
);
create index exploremoz_outbox_pending on exploremoz_internal.outbox (created_at, id)
  where delivered_at is null;
alter table exploremoz_internal.outbox enable row level security;
grant usage on schema exploremoz_internal to service_role;
grant select on exploremoz_internal.outbox to service_role;
grant update (delivered_at) on exploremoz_internal.outbox to service_role;

create function exploremoz_internal.enqueue() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  insert into exploremoz_internal.outbox (event_type, resource_id)
  values (tg_argv[0], new.id);
  return new;
end;
$$;
revoke all on function exploremoz_internal.enqueue() from public, anon, authenticated;
create trigger exploremoz_ticket_created after insert on public.exploremoz_support
for each row execute function exploremoz_internal.enqueue('support.created');
create trigger exploremoz_partner_started after insert on public.exploremoz_partner_applications
for each row execute function exploremoz_internal.enqueue('partner.started');

commit;
