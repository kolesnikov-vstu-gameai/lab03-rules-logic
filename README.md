# Лабораторная работа № 3. Логическая модель стелс-NPC на основе правил

Дисциплина «Игровой искусственный интеллект» · Максимум **20 баллов** (+5 за задание со звёздочкой)

**Студент:** ФИО, группа · **Вариант стека:** … · **Видео:** <ссылка> · **Отчёт:** `docs/report.md` → PDF

## Стек

Unity + C# (A) · Python + experta/pyke (B) · SWI-Prolog + pyswip (C) · Unity + Prolog (D)

## Что нужно сдать

- [ ] Движок правил с 10+ правилами
- [ ] 2+ стражника в сцене
- [ ] Лог фактов и сработавших правил по сценариям
- [ ] Видео каждого сценария
- [ ] Отчёт PDF 5–7 стр.: предикаты, правила, диаграммы сценариев

Полное задание, критерии оценки и типичные ошибки — в методических указаниях (ЛР № 3).

## Варианты в этом шаблоне

- `python/` — вариант B: собственный forward-chaining движок правил (+ тесты). Легко заменить на experta.
- `prolog/guard.pl` — вариант C: та же база знаний на SWI-Prolog; `python/src/rules/prolog_bridge.py` — вызов через pyswip.
- `unity/` — вариант A: C#-движок правил и интеграция со стражником из ЛР 1.

Оставьте один вариант. Сценарии для тестирования — в `scenarios/*.json`, логи вывода — в `results/`.

## Запуск (Python)

```bash
cd python && pip install -r requirements.txt   # или: make install
make check                        # линтер + тесты; все команды: make help
```

## Пример выполнения

**Где это в играх.** В Thief (1998) стражи реагируют на свет и шум по набору правил: игрок в тени не виден,
шаги по металлу слышны дальше, чем по ковру. Похожий индикатор освещённости есть в Splinter Cell. Реплики персонажей
в Left 4 Dead выбираются системой правил: из десятков фактов о ситуации («кто рядом», «сколько здоровья», «что только что
случилось») подбирается подходящая фраза. В F.E.A.R. враги строили планы действий по логическим предусловиям (GOAP).

**Зачем:** правила читаются как текст, их может менять геймдизайнер без переписывания кода, а по логу всегда видно,
почему NPC поступил именно так. Это и тренирует ЛР: база фактов, правила с приоритетами и объяснимый вывод.

В `python/src/rules/guard_rules.py` уже есть 4 правила на стражника. Пример того, как можно добрать до 10+:

| № | Правило | Если | То | Приоритет |
|---|---|---|---|---|
| 1 | see_player | `sees(G, player)` | `state(G, chase)` | 10 |
| 2 | raise_alarm | `state(G, chase)`, нет `alarm` | `alarm` | 8 |
| 3 | alarm_join | `alarm`, `state(G, patrol)` | `state(G, search)` | 7 |
| 4 | hear_noise | `hears(G, noise)`, `state(G, patrol)` | `state(G, investigate)` | 5 |
| 5 | lost_target | `state(G, chase)`, нет `sees(G, player)` | `state(G, search)`, `last_seen(G, Zone)` | 6 |
| 6 | dark_zone | `at(player, Z)`, нет `light_on(Z)` | `sees` не выводится, только `hears` | 9 |
| 7 | door_opened | `door_open(Z)` и раньше была закрыта | `hears(G, noise)` для стражей рядом | 4 |
| 8 | light_off | `at(G, Z)`, нет `light_on(Z)` | `state(G, investigate)`, цель — выключатель | 4 |
| 9 | search_timeout | `state(G, search)`, прошло 10 с | `state(G, patrol)` | 3 |
| 10 | alarm_reset | `alarm`, все стражи в `patrol` | снять `alarm` | 2 |
| 11 | return_post | `state(G, investigate)`, ничего не найдено | `state(G, patrol)` | 1 |

**Пример нового сценария** `scenarios/03_player_in_dark.json`:

```json
{"name": "player in dark zone near g1",
 "facts": [["at", "player", "hall"], ["at", "g1", "hall"], ["hears", "g1", "noise"]],
 "expect": {"g1": "investigate", "g2": "patrol"}}
```

**Пример лога вывода** (`results/03_player_in_dark.log`):

```text
facts: at(player,hall) at(g1,hall) hears(g1,noise) state(g1,patrol) state(g2,patrol)
fired: dark_zone_g1       → sees(g1,player) заблокирован
fired: hear_noise_g1      → state(g1,investigate)
result: g1=investigate g2=patrol   OK
```

Для каждого сценария в отчёте: исходные факты → цепочка сработавших правил → итоговые состояния, и видео того же сценария в сцене.

## Как сдавать

1. Работайте в этом репозитории, коммитьте по шагам (`step-1`, `step-2` …) — история коммитов учитывается.
2. Отчёт пишите в `docs/report.md` (черновик по разделам, 5–7 стр.), затем перенесите в официальный шаблон отчёта, принятый на кафедре, и экспортируйте в PDF (`docs/report.pdf`).
3. Видео — на YouTube/Диск, ссылку в README и в отчёт. Файлы видео в git не кладём.
4. Готовую работу отметьте тегом `git tag v1.0 && git push --tags` и создайте Release.
