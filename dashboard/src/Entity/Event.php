<?php

namespace Libero\Dashboard\Entity;

use DateTimeImmutable;
use DateTimeZone;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table
 */
final class Event
{
    /**
     * @ORM\Embedded(class="Aggregate")
     */
    private $aggregate;

    /**
     * @ORM\Column(type="datetime_immutable")
     */
    private $dateTime;

    /**
     * @ORM\Column(type="guid")
     * @ORM\Id
     */
    private $id;

    /**
     * @ORM\Column(type="string")
     */
    private $type;

    public function __construct(string $id, DateTimeImmutable $dateTime, string $type, Aggregate $aggregate)
    {
        $this->id = $id;
        $this->dateTime = $dateTime->setTimezone(new DateTimeZone('UTC'));
        $this->type = $type;
        $this->aggregate = $aggregate;
    }

    public function getAggregate() : Aggregate
    {
        return $this->aggregate;
    }

    public function getDateTime() : DateTimeImmutable
    {
        return $this->dateTime;
    }

    public function getId() : string
    {
        return $this->id;
    }

    public function getType() : string
    {
        return $this->type;
    }
}
