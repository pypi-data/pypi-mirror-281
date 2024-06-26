from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


# specifically test multi-hit abilities separately for now
class TestRotationBuilderMulti(TestClass):
    def __init__(self):
        self.__stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=708,
            job_class="test_job",
            version="test",
        )
        self.__skill_library = create_test_skill_library()

    @TestClass.is_a_test
    def test_multi_target_add_next(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_instant_gcd", targets=("t1", "t2"))

        # include priority and event id
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
        )
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_multi_target_add_instant(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1, "test_instant_gcd", targets=("t1", "t2"))

        # include priority and event id
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
        )
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_multi_target_add(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1, "test_gcd", targets=("t1", "t2"))

        # include priority and event id
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
        )
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @staticmethod
    def __extract_rb_q_info(q):
        result = []
        for r in q:
            tmp = (
                (r[1].primary, r[1].secondary),  # event times
                r[2].name,  # skill name
                r[5],
            )  # targets
            result.append(tmp)
        return frozenset(tuple(result))

    @TestClass.is_a_test
    def test_multi_target_dot_no_refresh(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_magical_dot_instant_gcd_short", targets=("t1", "t2"))

        expected = frozenset(
            (
                ((0, None), "test_magical_dot_instant_gcd_short", ("t1", "t2")),
                ((0, None), "test_magical_dot_tick", ("t1",)),
                ((0, None), "test_magical_dot_tick", ("t2",)),
                ((0, 3000), "test_magical_dot_tick", ("t1",)),
                ((0, 3000), "test_magical_dot_tick", ("t2",)),
                ((0, 6000), "test_magical_dot_tick", ("t1",)),
                ((0, 6000), "test_magical_dot_tick", ("t2",)),
            )
        )

        result = TestRotationBuilderMulti.__extract_rb_q_info(
            rb.get_skill_timing().get_q()
        )
        return self._compare_sets(result, expected)

    @TestClass.is_a_test
    def test_multi_target_dot_with_refresh(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            fight_start_time=0,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add(0, "test_magical_dot_instant_gcd_short", targets=("t1", "t2"))
        rb.add(5, "test_magical_dot_instant_gcd_short", targets=("t2",))

        expected = frozenset(
            (
                ((0, None), "test_magical_dot_instant_gcd_short", ("t1", "t2")),
                ((5000, None), "test_magical_dot_instant_gcd_short", ("t2",)),
                ((0, None), "test_magical_dot_tick", ("t1",)),
                ((0, None), "test_magical_dot_tick", ("t2",)),
                ((0, 3000), "test_magical_dot_tick", ("t1",)),
                ((0, 3000), "test_magical_dot_tick", ("t2",)),
                ((0, 6000), "test_magical_dot_tick", ("t1",)),
                ((5000, 6000), "test_magical_dot_tick", ("t2",)),
                ((5000, 9000), "test_magical_dot_tick", ("t2",)),
                ((5000, 12000), "test_magical_dot_tick", ("t2",)),
            )
        )

        result = TestRotationBuilderMulti.__extract_rb_q_info(
            rb.get_skill_timing().get_q()
        )
        return self._compare_sets(result, expected)
